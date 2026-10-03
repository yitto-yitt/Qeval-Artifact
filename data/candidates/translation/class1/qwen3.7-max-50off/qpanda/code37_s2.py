# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import QMachine, QProg, H, X, CNOT, Measure

def bv_algorithm(s):
    n = len(s)
    qm = QMachine()
    q = qm.alloc_qubits(n + 1)
    c = qm.alloc_cbits(n)
    
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
        
    result = qm.run(prog, 1)
    bitstrings = list(result.keys())
    return [bitstrings, result]
