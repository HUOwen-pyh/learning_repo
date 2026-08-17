"""指数伴随的有限 curry/uncurry 双射。"""
from __future__ import annotations
import itertools, sys
sys.stdout.reconfigure(encoding="utf-8")

X,A,B=(0,1),(0,1),(0,1)
def curry(table): return tuple(tuple(table[(x,a)] for a in A) for x in X)
def uncurry(curried): return {(x,a):curried[x][a] for x in X for a in A}

def main() -> None:
    tables=[]
    keys=[(x,a) for x in X for a in A]
    for vals in itertools.product(B,repeat=len(keys)): tables.append(dict(zip(keys,vals)))
    encoded={curry(t) for t in tables}
    assert len(tables)==len(encoded)==16
    assert all(uncurry(curry(t))==t for t in tables)
    assert all(curry(uncurry(c))==c for c in encoded)
    print("Hom(X×A,B) 与 Hom(X,B^A) 均有",len(encoded),"个元素")

if __name__ == "__main__": main()

# 动手改造：改变集合大小，验证两侧基数公式仍相同。
