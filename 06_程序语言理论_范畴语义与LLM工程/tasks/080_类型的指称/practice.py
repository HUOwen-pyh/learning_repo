"""第080晚：有限类型解释与函数空间枚举。"""
from itertools import product
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
BOOL=(False,True);NAT3=(0,1,2)
def function_space(domain,codomain):
    return [dict(zip(domain,outputs)) for outputs in product(codomain,repeat=len(domain))]
def member_arrow(mapping,domain,codomain):
    return set(mapping)==set(domain) and all(mapping[x] in codomain for x in domain)
def main():
    bb=function_space(BOOL,BOOL)
    assert len(bb)==4 and all(member_arrow(f,BOOL,BOOL) for f in bb)
    assert len(function_space(BOOL,NAT3))==9
    assert not member_arrow({False:False,True:"bad"},BOOL,BOOL)
    assert function_space((),BOOL)==[{}]                  # empty-domain boundary
    const_true={False:True,True:True};assert const_true in bb
    print("第080晚通过：有限基类型与箭头类型的集合解释正确。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
