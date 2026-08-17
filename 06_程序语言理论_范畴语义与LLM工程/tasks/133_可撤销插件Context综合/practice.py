"""覆盖四类状态，并对 apply 中途异常做逆序事务回滚的 MiniContext。"""
from __future__ import annotations

import sys
from collections.abc import Callable
from dataclasses import dataclass

sys.stdout.reconfigure(encoding="utf-8")

Undo = tuple[str, Callable[[], None]]
Apply = Callable[["Context", str, list[Undo]], None]


@dataclass(frozen=True)
class Snapshot:
    services: tuple[tuple[str, str], ...]
    listeners: tuple[tuple[str, str], ...]
    tools: tuple[tuple[str, str], ...]
    active_fibers: tuple[str, ...]


class Context:
    def __init__(self) -> None:
        self.services: dict[str, str] = {}
        self.listeners: list[tuple[str, str]] = []
        self.tools: dict[str, str] = {}
        self.active_fibers: set[str] = set()
        self.active: dict[str, list[Undo]] = {}
        self.requires: dict[str, set[str]] = {}
        self.order: list[str] = []
        self.rollback_log: list[str] = []

    @staticmethod
    def record(journal: list[Undo], label: str, undo: Callable[[], None]) -> None:
        journal.append((label, undo))

    def register_service(self, owner: str, name: str, journal: list[Undo]) -> None:
        if name in self.services:
            raise ValueError(f"duplicate service: {name}")
        self.services[name] = owner
        self.record(journal, f"service:{name}", lambda: self.services.pop(name))

    def register_listener(self, owner: str, event: str, journal: list[Undo]) -> None:
        item = (owner, event)
        self.listeners.append(item)
        self.record(journal, f"listener:{owner}", lambda: self.listeners.remove(item))

    def register_tool(self, owner: str, name: str, journal: list[Undo]) -> None:
        if name in self.tools:
            raise ValueError(f"duplicate tool: {name}")
        self.tools[name] = owner
        self.record(journal, f"tool:{owner}", lambda: self.tools.pop(name))

    def mount(self, name: str, requires: set[str], apply: Apply) -> None:
        missing = requires - self.services.keys()
        if missing:
            raise LookupError(f"missing services: {sorted(missing)}")
        journal: list[Undo] = []
        self.active_fibers.add(name)
        self.record(journal, f"fiber:{name}", lambda: self.active_fibers.remove(name))
        try:
            apply(self, name, journal)
        except Exception:
            self._rollback(journal)
            raise
        self.active[name] = journal
        self.requires[name] = set(requires)
        self.order.append(name)
        assert self.valid()

    def _rollback(self, journal: list[Undo]) -> None:
        for label, undo in reversed(journal):
            undo()
            self.rollback_log.append(label)

    def unmount(self, name: str) -> None:
        if name not in self.active:
            return
        provided = {service for service, owner in self.services.items() if owner == name}
        for candidate in reversed(self.order.copy()):
            if candidate != name and candidate in self.active and self.requires[candidate] & provided:
                self.unmount(candidate)
        self._rollback(self.active.pop(name))
        self.requires.pop(name)
        self.order.remove(name)
        assert self.valid()

    def dispose(self) -> None:
        for name in reversed(self.order.copy()):
            self.unmount(name)

    def snapshot(self) -> Snapshot:
        return Snapshot(
            tuple(sorted(self.services.items())),
            tuple(self.listeners),
            tuple(sorted(self.tools.items())),
            tuple(sorted(self.active_fibers)),
        )

    def valid(self) -> bool:
        owners = set(self.active)
        registrations = (
            set(self.services.values())
            | {owner for owner, _ in self.listeners}
            | set(self.tools.values())
        )
        dependencies_hold = all(req <= self.services.keys() for req in self.requires.values())
        return registrations <= owners and self.active_fibers == owners and dependencies_hold


def provider(ctx: Context, owner: str, journal: list[Undo]) -> None:
    ctx.register_service(owner, "llm", journal)


def consumer(ctx: Context, owner: str, journal: list[Undo]) -> None:
    ctx.register_listener(owner, "message", journal)
    ctx.register_tool(owner, "search", journal)


def broken(ctx: Context, owner: str, journal: list[Undo]) -> None:
    ctx.register_listener(owner, "partial", journal)
    ctx.register_tool(owner, "broken-tool", journal)
    raise RuntimeError("apply failed after two registrations")


def main() -> None:
    context = Context()
    context.mount("provider", set(), provider)
    context.mount("consumer", {"llm"}, consumer)
    assert context.snapshot() == Snapshot(
        (("llm", "provider"),),
        (("consumer", "message"),),
        (("search", "consumer"),),
        ("consumer", "provider"),
    )

    before_failure = context.snapshot()
    context.rollback_log.clear()
    try:
        context.mount("broken", {"llm"}, broken)
    except RuntimeError:
        pass
    else:
        raise AssertionError("中途 apply 异常必须向上传播")
    assert context.snapshot() == before_failure, "失败 apply 不得留下四类状态残留"
    assert context.rollback_log == [
        "tool:broken",
        "listener:broken",
        "fiber:broken",
    ], "回滚必须严格逆注册顺序"

    context.unmount("provider")  # 自动先卸载依赖它的 consumer。
    assert context.snapshot() == Snapshot((), (), (), ())
    context.mount("provider", set(), provider)
    context.mount("consumer", {"llm"}, consumer)
    context.dispose()
    assert context.snapshot() == Snapshot((), (), (), ())
    assert not context.active and not context.order
    print("四类状态、依赖卸载与 apply 异常逆序回滚不变量通过")


if __name__ == "__main__":
    main()

# 动手改造：让 disposer 自身抛错，设计“继续清理并聚合错误”的策略。
