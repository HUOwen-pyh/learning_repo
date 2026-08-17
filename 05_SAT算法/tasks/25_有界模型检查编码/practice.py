"""Bounded model checking of a two-bit counter via explicit SAT-style search."""
from itertools import product

def bits(value,width=2):return tuple(bool(value>>i&1) for i in range(width))
def value(state):return sum(int(b)<<i for i,b in enumerate(state))
def transition(a,b):return value(b)==(value(a)+1)%4
def initial(s):return value(s)==0
def bad(s):return value(s)==3

def bmc(k):
    states=list(product((False,True),repeat=2))
    for trace in product(states,repeat=k+1):
        if initial(trace[0]) and all(transition(a,b) for a,b in zip(trace,trace[1:])) and any(bad(s) for s in trace):
            return trace
    return None

def encode_var(time,bit,width=2):return 1+time*width+bit

if __name__=="__main__":
    assert bmc(0) is None and bmc(1) is None and bmc(2) is None
    trace=bmc(3)
    print("shortest bad trace:",[value(s) for s in trace])
    assert [value(s) for s in trace]==[0,1,2,3]
    assert all(transition(a,b) for a,b in zip(trace,trace[1:]))
    ids={encode_var(t,b) for t in range(4) for b in range(2)}
    assert len(ids)==8
    print("UNSAT at k=2 means only: no counterexample of length <=2.")
    # Hands-on: generate actual Tseitin CNF for each transition and decode its model.

