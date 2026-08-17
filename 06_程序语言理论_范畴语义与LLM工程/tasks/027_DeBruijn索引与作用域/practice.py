"""第 027 晚：具名项转 locally nameless de Bruijn 项。"""
from __future__ import annotations

import sys
from dataclasses import dataclass

sys.stdout.reconfigure(encoding="utf-8")


@dataclass(frozen=True)
class NVar: name: str
@dataclass(frozen=True)
class NLam: param: str; body: "Named"
@dataclass(frozen=True)
class NApp: fn: "Named"; arg: "Named"
Named = NVar | NLam | NApp


@dataclass(frozen=True)
class Bound: index: int
@dataclass(frozen=True)
class Free: name: str
@dataclass(frozen=True)
class DBLam: body: "DB"
@dataclass(frozen=True)
class DBApp: fn: "DB"; arg: "DB"
DB = Bound | Free | DBLam | DBApp


def to_db(t: Named, binders: tuple[str, ...] = ()) -> DB:
    if isinstance(t, NVar):
        for index, name in enumerate(reversed(binders)):
            if t.name == name:
                return Bound(index)
        return Free(t.name)
    if isinstance(t, NLam):
        return DBLam(to_db(t.body, binders + (t.param,)))
    if isinstance(t, NApp):
        return DBApp(to_db(t.fn, binders), to_db(t.arg, binders))
    raise TypeError("非法具名项")


def well_scoped(t: DB, depth: int = 0) -> bool:
    if isinstance(t, Bound):
        return 0 <= t.index < depth
    if isinstance(t, Free):
        return True
    if isinstance(t, DBLam):
        return well_scoped(t.body, depth + 1)
    return well_scoped(t.fn, depth) and well_scoped(t.arg, depth)


a = NLam("x", NLam("y", NApp(NVar("x"), NVar("y"))))
b = NLam("a", NLam("b", NApp(NVar("a"), NVar("b"))))
assert to_db(a) == to_db(b)                                    # 正例：alpha 等价
assert to_db(NLam("x", NVar("y"))) != to_db(NLam("y", NVar("y")))
assert well_scoped(DBLam(Bound(0))) and not well_scoped(Bound(0))  # 边界/反例

# 动手改造：实现 from_db，并用自动生成的新名字验证往返结果 alpha 等价。
print("027 通过：绑定结构已转换为可检查的 de Bruijn 索引。")

