"""Pairwise and Sinz sequential at-most-one encodings, projection-checked."""
from itertools import product

def pairwise_amo(xs):
    return [(-xs[i],-xs[j]) for i in range(len(xs)) for j in range(i+1,len(xs))],max(xs,default=0)

def sequential_amo(xs):
    if len(xs)<=1:return [],max(xs,default=0)
    next_var=max(xs)+1;s=list(range(next_var,next_var+len(xs)-1));c=[]
    c.append((-xs[0],s[0]))
    for i in range(1,len(xs)-1):
        c += [(-xs[i],s[i]),(-s[i-1],s[i]),(-xs[i],-s[i-1])]
    c.append((-xs[-1],-s[-1]))
    return c,s[-1]

def sat_with_fixed(cnf,nvars,fixed):
    free=[v for v in range(1,nvars+1) if v not in fixed]
    return any(all(any((fixed|dict(zip(free,bits)))[abs(l)]==(l>0) for l in c) for c in cnf)
               for bits in product((False,True),repeat=len(free)))

if __name__=="__main__":
    print("n pairwise_clauses sequential_clauses sequential_aux")
    for n in range(1,9):
        xs=list(range(1,n+1));pc,pmax=pairwise_amo(xs);sc,smax=sequential_amo(xs)
        for bits in product((False,True),repeat=n):
            fixed=dict(zip(xs,bits));condition=sum(bits)<=1
            assert sat_with_fixed(pc,pmax,fixed)==condition
            assert sat_with_fixed(sc,smax,fixed)==condition
        print(n,len(pc),len(sc),max(0,smax-n))
    exactly_one,_=sequential_amo([1,2,3]);exactly_one.append((1,2,3))
    assert not sat_with_fixed(exactly_one,5,{1:False,2:False,3:False})
    # Hands-on: encode at-most-k with a two-dimensional sequential counter.

