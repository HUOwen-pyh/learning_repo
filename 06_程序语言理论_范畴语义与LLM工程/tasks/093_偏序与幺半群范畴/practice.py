"""第093晚：preorder thin category 与 monoid one-object category。"""
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
def preorder_category(xs,leq):
    arrows={(a,b) for a in xs for b in xs if leq(a,b)}
    comp={((b,c),(a,b)):(a,c) for a,b in arrows for b2,c in arrows if b==b2}
    return arrows,comp
def check_thin(xs,arrows,comp):
    return all((x,x) in arrows for x in xs) and all((a,c) in arrows and comp[((b,c),(a,b))]==(a,c) for a,b in arrows for b2,c in arrows if b==b2)
def check_monoid(elements,op,e):
    return e in elements and all(op(e,a)==a==op(a,e) for a in elements) and all(op(op(a,b),c)==op(a,op(b,c)) for a in elements for b in elements for c in elements)
def main():
    xs=range(4);arrows,comp=preorder_category(xs,lambda a,b:a<=b)
    assert check_thin(xs,arrows,comp) and len([a for a in arrows if a==(1,2)])==1
    elems={0,1,2};op=lambda a,b:(a+b)%3
    assert check_monoid(elems,op,0)
    bad=lambda a,b:(a+2*b)%3;assert not check_monoid(elems,bad,0)
    ar0,co0=preorder_category([],lambda a,b:True);assert ar0==set() and check_thin([],ar0,co0)
    print("第093晚通过：thin category 与单对象 monoid law 均验证。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
