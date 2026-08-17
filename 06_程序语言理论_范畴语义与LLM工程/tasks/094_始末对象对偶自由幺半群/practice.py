"""第094晚：始末对象、opposite 与 free-monoid fold。"""
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
def arrows_chain(n):return {(a,b) for a in range(n) for b in range(n) if a<=b}
def initial(objects,arrows):
    return [x for x in objects if all((x,y) in arrows for y in objects)]
def terminal(objects,arrows):
    return [x for x in objects if all((y,x) in arrows for y in objects)]
def opposite(arrows):return {(b,a) for a,b in arrows}
def fold_word(word,image,op,e):
    out=e
    for letter in word:out=op(out,image[letter])
    return out
def main():
    objs=set(range(4));arr=arrows_chain(4)
    assert initial(objs,arr)==[0] and terminal(objs,arr)==[3]
    op=opposite(arr);assert initial(objs,op)==[3] and terminal(objs,op)==[0]
    image={"a":2,"b":3};plus=lambda x,y:x+y
    assert fold_word(("a","b","a"),image,plus,0)==7
    u=("a","b");v=("b",)
    assert fold_word(u+v,image,plus,0)==plus(fold_word(u,image,plus,0),fold_word(v,image,plus,0))
    assert fold_word((),image,plus,0)==0                  # empty word boundary
    print("第094晚通过：对偶交换始末对象，自由 word fold 满足同态律。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
