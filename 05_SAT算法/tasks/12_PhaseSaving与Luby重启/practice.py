"""Luby restart budgets and phase saving."""
def luby(index):
    """1-indexed: 1,1,2,1,1,2,4,..."""
    assert index>=1
    k=1
    while (1<<k)-1<index:k+=1
    if index==(1<<k)-1:return 1<<(k-1)
    return luby(index-(1<<(k-1))+1)

class RestartState:
    def __init__(self):
        self.saved_phase={};self.trail=[];self.root_size=0;self.learned=[]
    def assign(self,var,value):
        self.saved_phase[var]=value;self.trail.append(var if value else -var)
    def restart(self):
        del self.trail[self.root_size:]
    def preferred(self,var):
        return self.saved_phase.get(var,True)

if __name__=="__main__":
    sequence=[luby(i) for i in range(1,17)]
    expected=[1,1,2,1,1,2,4,1,1,2,1,1,2,4,8,1]
    print("Luby:",sequence)
    assert sequence==expected
    s=RestartState();s.assign(1,True);s.root_size=1
    s.learned.append((-1,2));s.assign(2,False);s.assign(3,True)
    s.restart()
    assert s.trail==[1] and s.learned==[(-1,2)]
    assert s.preferred(2) is False and s.preferred(3) is True
    budgets=[100*luby(i) for i in range(1,10)]
    print("conflict budgets:",budgets)
    # Hands-on: compare Luby and geometric budgets under a synthetic best cutoff.

