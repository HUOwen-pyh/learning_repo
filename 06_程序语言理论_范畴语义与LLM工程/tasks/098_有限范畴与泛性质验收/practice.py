"""第098晚：finite-poset category 的始末对象、product/coproduct 搜索。"""
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
class PosetCategory:
    def __init__(self,objects,leq):self.objects=tuple(objects);self.leq=leq
    def check(self):
        O=self.objects
        return all(self.leq(x,x) for x in O) and all(not(self.leq(x,y) and self.leq(y,x)) or x==y for x in O for y in O) and all(not(self.leq(x,y) and self.leq(y,z)) or self.leq(x,z) for x in O for y in O for z in O)
    def initial(self):
        return next((x for x in self.objects if all(self.leq(x,y) for y in self.objects)),None)
    def terminal(self):
        return next((x for x in self.objects if all(self.leq(y,x) for y in self.objects)),None)
    def product(self,a,b):
        lowers=[x for x in self.objects if self.leq(x,a) and self.leq(x,b)]
        return next((p for p in lowers if all(self.leq(x,p) for x in lowers)),None)
    def coproduct(self,a,b):
        uppers=[x for x in self.objects if self.leq(a,x) and self.leq(b,x)]
        return next((p for p in uppers if all(self.leq(p,x) for x in uppers)),None)
def main():
    O=("0","a","b","1")
    def diamond(x,y):return x==y or x=="0" or y=="1"
    c=PosetCategory(O,diamond);assert c.check()
    assert c.initial()=="0" and c.terminal()=="1"
    assert c.product("a","b")=="0" and c.coproduct("a","b")=="1"
    assert c.product("a","1")=="a" and c.coproduct("0","b")=="b"
    # Two incomparable maximal lower bounds p,q: no greatest lower bound.
    D=("p","q","a","b")
    rel={("p","a"),("p","b"),("q","a"),("q","b")}
    no_meet=PosetCategory(D,lambda x,y:x==y or (x,y) in rel)
    assert no_meet.check() and no_meet.product("a","b") is None
    singleton=PosetCategory(("x",),lambda x,y:True)
    assert singleton.initial()==singleton.terminal()=="x"
    print("第098晚通过：diamond 的泛性质成立，缺失 meet 的负例被识别。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
