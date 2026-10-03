# EVAL_META: task_id=56, framework=qpanda, class=1
from pyqpanda3.core import QuantumMachine, QProg, X, Measure

def not_gate(a):
    qm = QuantumMachine()
    q = qm.qAlloc_many(8)
    c = qm.cAlloc_many(8)
    prog = QProg()
    
    a_bin = format(a, "08b")
    for i in range(8):
        if a_bin[7-i] == '0':
            prog << X(q[i])
            
    for i in range(8):
        prog << Measure(q[i], c[i])
        
    counts = qm.run(prog, 1000)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
