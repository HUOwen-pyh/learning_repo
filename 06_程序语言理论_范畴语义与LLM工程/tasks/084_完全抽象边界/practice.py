"""第084晚：只能观察奇偶性的语言与过细 exact-int 模型。"""
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
CONTEXTS=(0,2,4)  # contexts may add only even constants
def observe(n):return n%2
def ctx_equiv(a,b):
    return all(observe(a+k)==observe(b+k) for k in CONTEXTS)
def exact_den(n):return n
def parity_den(n):return n%2
def main():
    assert ctx_equiv(0,2) and exact_den(0)!=exact_den(2)   # too fine: not full abstract
    assert parity_den(0)==parity_den(2)
    assert not ctx_equiv(0,1)
    assert exact_den(3)==exact_den(3) and ctx_equiv(3,3)   # reflexive boundary
    values=range(6)
    assert all((parity_den(a)==parity_den(b))==ctx_equiv(a,b) for a in values for b in values)
    print("第084晚通过：过细模型反例成立；parity 模型匹配给定观察。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
