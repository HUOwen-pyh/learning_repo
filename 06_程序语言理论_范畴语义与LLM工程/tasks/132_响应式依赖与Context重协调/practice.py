"""逐事件维护 provider 与插件生命周期的响应式协调器。"""
from __future__ import annotations

import sys
from dataclasses import dataclass

sys.stdout.reconfigure(encoding="utf-8")


@dataclass(frozen=True)
class Plugin:
    name: str
    requires: frozenset[str]
    provides: frozenset[str]


class Resolver:
    def __init__(self, plugins: list[Plugin]) -> None:
        self.plugins = plugins  # 已按拓扑序声明。
        self.providers: set[str] = set()
        self.active: list[str] = []
        self.events: list[tuple[str, str]] = []

    def add_provider(self, service: str) -> None:
        self.providers.add(service)
        self.events.append(("provider:add", service))
        self.reconcile()

    def remove_provider(self, service: str) -> None:
        self.providers.discard(service)
        self.events.append(("provider:remove", service))
        self.reconcile()

    def desired_order(self) -> list[str]:
        available = set(self.providers)
        desired: list[str] = []
        for plugin in self.plugins:
            if plugin.requires <= available:
                desired.append(plugin.name)
                available |= plugin.provides
        return desired

    def reconcile(self) -> None:
        desired = self.desired_order()
        desired_set = set(desired)

        # 先按当前拓扑序的反序卸载失效 consumer。
        for name in reversed(self.active.copy()):
            if name not in desired_set:
                self.events.append(("unmount", name))
                self.active.remove(name)

        # 再按拓扑序挂载新近可用的插件。
        for name in desired:
            if name not in self.active:
                self.events.append(("mount", name))
                self.active.append(name)
        assert self.invariant()

    def capabilities(self) -> set[str]:
        result = set(self.providers)
        by_name = {plugin.name: plugin for plugin in self.plugins}
        for name in self.active:
            result |= by_name[name].provides
        return result

    def invariant(self) -> bool:
        available = set(self.providers)
        by_name = {plugin.name: plugin for plugin in self.plugins}
        for name in self.active:
            plugin = by_name[name]
            if not plugin.requires <= available:
                return False
            available |= plugin.provides
        return True


def main() -> None:
    resolver = Resolver(
        [
            Plugin("http-plugin", frozenset({"credentials"}), frozenset({"http"})),
            Plugin("search-plugin", frozenset({"http"}), frozenset({"search-tool"})),
        ]
    )
    resolver.add_provider("credentials")
    assert resolver.active == ["http-plugin", "search-plugin"]
    assert resolver.capabilities() == {"credentials", "http", "search-tool"}

    resolver.remove_provider("credentials")
    assert resolver.active == []
    assert resolver.events[-2:] == [
        ("unmount", "search-plugin"),
        ("unmount", "http-plugin"),
    ]

    resolver.add_provider("credentials")
    assert resolver.active == ["http-plugin", "search-plugin"]
    assert resolver.events[-2:] == [
        ("mount", "http-plugin"),
        ("mount", "search-plugin"),
    ]
    print("provider add/remove、拓扑挂载与逆拓扑卸载事件序列通过")


if __name__ == "__main__":
    main()

# 动手改造：加入两个可替代的 http provider，验证只在最后一个消失时卸载 consumer。
