"""第074晚：有限 powerset CPO 上的链、sup 与连续性方程。"""
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
def is_chain(xs):return all(a<=b or b<=a for a in xs for b in xs)
def sup(xs):
    out=frozenset()
    for x in xs:out|=x
    return out
def preserves_chain_sup(f,chain):
    if not is_chain(chain):raise ValueError("not a chain")
    return f(sup(chain))==sup([f(x) for x in chain])
def main():
    chain=[frozenset(),frozenset({"a"}),frozenset({"a","b"})]
    f=lambda x:x|{"c"}
    assert is_chain(chain) and sup(chain)==frozenset({"a","b"})
    assert preserves_chain_sup(f,chain)
    assert preserves_chain_sup(f,[frozenset()])            # singleton boundary
    bad=[frozenset({"a"}),frozenset({"b"})]
    assert not is_chain(bad)
    try:preserves_chain_sup(f,bad)
    except ValueError:pass
    else:raise AssertionError("non-chain accepted")
    complement=lambda x:frozenset({"a","b"}-set(x))
    assert not preserves_chain_sup(complement,chain)        # nonmonotone negative
    print("第074晚通过：链上确界与连续性方程在有限模型中成立。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
