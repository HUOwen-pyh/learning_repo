"""Trail, decision levels, reasons, qhead, and rollback."""
class Trail:
    def __init__(self):
        self.values={};self.level={};self.reason={}
        self.trail=[];self.trail_lim=[];self.qhead=0
    @property
    def decision_level(self):return len(self.trail_lim)
    def new_level(self):self.trail_lim.append(len(self.trail))
    def enqueue(self,lit,reason=None):
        var=abs(lit);value=lit>0
        if var in self.values:return self.values[var]==value
        self.values[var]=value;self.level[var]=self.decision_level
        self.reason[var]=reason;self.trail.append(lit);return True
    def backtrack(self,target):
        assert 0<=target<=self.decision_level
        cut=len(self.trail) if target==self.decision_level else self.trail_lim[target]
        for lit in reversed(self.trail[cut:]):
            v=abs(lit);del self.values[v];del self.level[v];del self.reason[v]
        del self.trail[cut:];del self.trail_lim[target:]
        self.qhead=min(self.qhead,len(self.trail))
    def check(self):
        assert len({abs(l) for l in self.trail})==len(self.trail)
        assert set(self.values)=={abs(l) for l in self.trail}
        assert all(self.values[abs(l)]==(l>0) for l in self.trail)

if __name__=="__main__":
    t=Trail();assert t.enqueue(1,("root",))
    t.qhead=1;t.new_level();assert t.enqueue(-2,None)
    assert t.enqueue(3,(2,3));t.qhead=3
    t.new_level();assert t.enqueue(4,None);assert not t.enqueue(-4)
    print("before:",t.trail,t.level,t.reason,t.trail_lim)
    t.backtrack(1);t.check()
    print("after backtrack(1):",t.trail,t.level,t.trail_lim,"qhead",t.qhead)
    assert t.trail==[1,-2,3] and 4 not in t.values and t.decision_level==1
    t.backtrack(0);t.check();assert t.trail==[1]
    # Hands-on: add cancel_until and verify root propagations survive every restart.

