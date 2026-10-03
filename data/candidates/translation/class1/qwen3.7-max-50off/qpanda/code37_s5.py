# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import QMachine, QProg, X, H, CNOT, Measure

def bv_algorithm(s):
    n = len(s)
    qvm = QMachine()
    q = qvm.qAlloc(n + 1)
    c = qvm.cAlloc(n)
    
    prog = QProg()
    prog << X(q[n])
    for i in range(n + 1):
        prog << H(q[i])
        
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << CNOT(q[index], q[n])
            
    for i in range(n):
        prog << H(q[i])
        
    for i in range(n):
        prog << Measure(q[i], c[i])
        
    result = qvm.run_with_config(prog, shots=1)
    bitstrings = list(result.keys())
    return [bitstrings, result]
