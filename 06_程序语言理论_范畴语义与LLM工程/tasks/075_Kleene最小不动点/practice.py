"""第075晚：Kleene iteration 计算有限图可达闭包。"""
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
GRAPH={"s":{"a"},"a":{"b"},"b":{"c"},"c":set(),"u":{"u"}}
def F(x):
    out={"s"}
    for n in x:out|=GRAPH.get(n,set())
    return frozenset(out)
def kleene(limit=20):
    x=frozenset();chain=[x]
    for _ in range(limit):
        y=F(x);chain.append(y)
        if y==x:return chain
        if not x<=y:raise AssertionError("not increasing")
        x=y
    raise RuntimeError("no finite stabilization")
def main():
    chain=kleene()
    assert chain[0]==frozenset()
    assert chain[-1]==frozenset({"s","a","b","c"})
    assert F(chain[-1])==chain[-1]
    assert "u" not in chain[-1]                            # unreachable cycle
    assert len(kleene())==6                                # includes bottom and fixed repeat
    assert F(frozenset())==frozenset({"s"})               # boundary
    print("第075晚通过：从 bottom 得到最小可达不动点，排除不可达环。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
