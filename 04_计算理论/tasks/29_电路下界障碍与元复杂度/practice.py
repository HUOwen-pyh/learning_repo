"""第29晚：极小真值表的公式尺寸枚举（MCSP 的教学缩影）。"""

def variable_table(n,index):
    table = 0
    for assignment in range(1<<n):
        if assignment>>index & 1:
            table |= 1<<assignment
    return table

def minimum_formula_sizes(n,max_size=12):
    rows = 1<<n
    mask = (1<<rows)-1
    exact = [set() for _ in range(max_size+1)]
    exact[0] = {0,mask} | {variable_table(n,i) for i in range(n)}
    minimum = {f:0 for f in exact[0]}
    for size in range(1,max_size+1):
        candidates = {(~f)&mask for f in exact[size-1]}
        for left_size in range(size):
            right_size = size-1-left_size
            for a in exact[left_size]:
                for b in exact[right_size]:
                    candidates.add(a&b); candidates.add(a|b)
        exact[size] = {f for f in candidates if f not in minimum}
        for f in exact[size]:
            minimum[f]=size
        if len(minimum)==1<<rows:
            break
    return minimum,exact

def table_from_predicate(n,predicate):
    return sum(int(predicate(tuple((a>>i)&1 for i in range(n))))<<a for a in range(1<<n))

if __name__ == "__main__":
    n=3
    minimum,exact = minimum_formula_sizes(n)
    parity = table_from_predicate(n,lambda bits:sum(bits)%2)
    majority = table_from_predicate(n,lambda bits:sum(bits)>=2)
    print("new functions by formula gate size:",[len(x) for x in exact])
    print("covered truth tables:",len(minimum),"/",1<<(1<<n))
    print("parity size:",minimum.get(parity,">12"),"majority size:",minimum.get(majority,">12"))
    assert majority in minimum and parity in minimum
    print("OPEN: this finite formula enumeration says nothing about MCSP NP-completeness.")
    # 动手改造：移除 OR 或常量，记录基底变化如何改变精确尺寸。

