# EVAL_META: task_id=145, framework=qpanda2, class=3
import pyqpanda as pq
from pyqpanda import *
import math

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)  # Assuming max 10 qubits for safety

def qft_inverse(n):
    qubits_local = qubits[:n]
    prog = pq.QProg()
    
    # Apply inverse QFT: reverse order of operations from normal QFT
    for i in range(n):
        # Apply inverse H gate (which is same as H since H^2 = I)
        prog << H(qubits_local[n-1-i])
        
        # Apply inverse controlled rotations
        for j in range(i+1, n):
            angle = -math.pi / (2 ** (j-i))
            prog << CR(qubits_local[n-1-j], qubits_local[n-1-i], angle)
    
    return prog

machine.finalize()
