"""自由幺半群的唯一 fold 延拓。"""
from __future__ import annotations
from functools import reduce
import sys
sys.stdout.reconfigure(encoding="utf-8")

def extend(generator_map, combine, unit, word):
    return reduce(combine,(generator_map(x) for x in word),unit)

def main() -> None:
    words=[[],["a"],["a","b"],["b","a","b"]]
    length=lambda w:extend(lambda _:1,lambda a,b:a+b,0,w)
    render=lambda w:extend(str,lambda a,b:a+b,"",w)
    for u in words:
        for v in words:
            assert length(u+v)==length(u)+length(v)
            assert render(u+v)==render(u)+render(v)
    bad=lambda w:extend(lambda _:1,lambda a,b:a+b,1,w)
    assert bad([])!=0
    print("自由幺半群 fold 的单位与拼接同态律通过")

if __name__ == "__main__": main()

# 动手改造：目标换成矩阵乘法幺半群，验证同一唯一延拓模式。
