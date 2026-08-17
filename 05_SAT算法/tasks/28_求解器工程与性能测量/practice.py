"""Operation-count benchmark: copying DPLL versus trail-style assignment."""
import cProfile,pstats,io,random,statistics

def verify(cnf,m,counter):
    for c in cnf:
        counter["literal_checks"]+=len(c)
        if not any(m.get(abs(l))==(l>0) for l in c):return False
    return True

def copying_search(cnf,n,assignment=None,stats=None):
    assignment={} if assignment is None else assignment
    stats={"nodes":0,"dict_copies":0,"literal_checks":0} if stats is None else stats
    stats["nodes"]+=1
    if len(assignment)==n:return verify(cnf,assignment,stats)
    v=len(assignment)+1
    for b in (False,True):
        child=dict(assignment);stats["dict_copies"]+=1;child[v]=b
        if copying_search(cnf,n,child,stats):return True
    return False

def trail_search(cnf,n,a,stats):
    stats["nodes"]+=1
    if len(a)==n:return verify(cnf,a,stats)
    v=len(a)+1
    for b in (False,True):
        a[v]=b
        if trail_search(cnf,n,a,stats):return True
        del a[v]
    return False

if __name__=="__main__":
    rng=random.Random(28);n=12
    cnf=tuple(tuple(rng.choice((-1,1))*rng.randint(1,n) for _ in range(3)) for _ in range(55))
    s1={"nodes":0,"dict_copies":0,"literal_checks":0};a1=copying_search(cnf,n,stats=s1)
    s2={"nodes":0,"dict_copies":0,"literal_checks":0};a2=trail_search(cnf,n,{},s2)
    assert a1==a2 and s1["nodes"]==s2["nodes"]
    print("copying:",s1,"trail:",s2)
    assert s1["dict_copies"]>0 and s2["dict_copies"]==0
    profiler=cProfile.Profile();profiler.enable();trail_search(cnf,n,{}, {"nodes":0,"dict_copies":0,"literal_checks":0});profiler.disable()
    stream=io.StringIO();pstats.Stats(profiler,stream=stream).sort_stats("tottime").print_stats(3)
    print(stream.getvalue())
    # Hands-on: repeat 11 times and report median wall time plus operation counts.

