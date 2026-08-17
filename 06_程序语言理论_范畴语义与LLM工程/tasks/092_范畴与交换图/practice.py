"""第092晚：有限范畴 law checker。动手改造：生成离散范畴。"""
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Arr:name:str;src:str;dst:str
class Category:
    def __init__(self,objects,arrows,ids,comp):
        self.objects=set(objects);self.arrows={a.name:a for a in arrows};self.ids=ids;self.comp=comp
    def check(self):
        if set(self.ids)!=self.objects:return False
        for o,i in self.ids.items():
            if i not in self.arrows or (self.arrows[i].src,self.arrows[i].dst)!=(o,o):return False
        # 先验证复合表本身，后面的单位律/结合律才能安全引用结果。
        # comp[(g,f)] 表示 g∘f，因此结果必须是 f.src → g.dst。
        for (g_name,f_name),result_name in self.comp.items():
            if g_name not in self.arrows or f_name not in self.arrows:return False
            g,f=self.arrows[g_name],self.arrows[f_name]
            if f.dst!=g.src:return False
            if result_name not in self.arrows:return False
            result=self.arrows[result_name]
            if (result.src,result.dst)!=(f.src,g.dst):return False
        for f in self.arrows.values():
            if f.src not in self.objects or f.dst not in self.objects:return False
            if self.comp.get((self.ids[f.dst],f.name))!=f.name:return False
            if self.comp.get((f.name,self.ids[f.src]))!=f.name:return False
        for f in self.arrows.values():
            for g in self.arrows.values():
                if f.dst==g.src and (g.name,f.name) not in self.comp:return False
        for f in self.arrows.values():
            for g in self.arrows.values():
                for h in self.arrows.values():
                    if f.dst==g.src and g.dst==h.src:
                        gf=self.comp[(g.name,f.name)];hg=self.comp[(h.name,g.name)]
                        if self.comp[(h.name,gf)]!=self.comp[(hg,f.name)]:return False
        return True
def chain():
    arr=[Arr("i0","0","0"),Arr("i1","1","1"),Arr("i2","2","2"),Arr("f","0","1"),Arr("g","1","2"),Arr("h","0","2")]
    comp={}
    for a in arr:
        comp[({"0":"i0","1":"i1","2":"i2"}[a.dst],a.name)]=a.name
        comp[(a.name,{"0":"i0","1":"i1","2":"i2"}[a.src])]=a.name
    comp[("g","f")]="h"
    return Category({"0","1","2"},arr,{"0":"i0","1":"i1","2":"i2"},comp)
def main():
    c=chain();assert c.check() and c.comp[("g","f")]=="h"
    bad=chain();del bad.comp[("g","f")];assert not bad.check()
    missing_result=chain();missing_result.comp[("g","f")]="不存在的箭头"
    assert not missing_result.check()                              # 结果必须存在
    wrong_endpoints=chain();wrong_endpoints.comp[("g","f")]="i0"
    assert not wrong_endpoints.check()                             # 存在但端点错误
    one=Category({"x"},[Arr("ix","x","x")],{"x":"ix"},{("ix","ix"):"ix"})
    assert one.check()
    print("第092晚通过：closure、单位律、结合律与缺失复合反例已检查。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
