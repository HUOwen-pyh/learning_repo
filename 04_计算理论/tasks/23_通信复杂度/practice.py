"""第23晚：函数矩阵与最大 fooling set 的小规模搜索。"""
from itertools import combinations
from math import ceil, log2

def equality(x,y):
    return x == y

def disjoint(x,y):
    return (x & y) == 0

def greater_than(x,y):
    return x > y

def is_fooling_set(entries, function, value):
    for i,(x,y) in enumerate(entries):
        if function(x,y) != value:
            return False
        for x2,y2 in entries[i+1:]:
            if function(x,y2) == value and function(x2,y) == value:
                return False
    return True

def maximum_fooling_set(domain, function):
    for value in (0,1):
        entries = [(x,y) for x in domain for y in domain if function(x,y) == bool(value)]
        for size in range(len(entries),0,-1):
            for chosen in combinations(entries,size):
                if is_fooling_set(chosen,function,bool(value)):
                    yield size,bool(value),chosen
                    break
            else:
                continue
            break

if __name__ == "__main__":
    domain = range(4)  # 两比特输入
    for name,fn in [("EQ",equality),("DISJ",disjoint),("GT",greater_than)]:
        candidates = list(maximum_fooling_set(domain,fn))
        size,value,witness = max(candidates,key=lambda x:x[0])
        lower = ceil(log2(size))
        print(f"{name}: fooling set size={size}, value={value}, "
              f"deterministic lower bound>={lower} bits, witness={witness}")
        assert is_fooling_set(witness,fn,value)
    # 动手改造：令输入为3比特；用回溯最大团替代全组合，比较搜索量。
