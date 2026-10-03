# EVAL_META: task_id=145, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import QProg, Qubit, CBit
import math

def qft_inverse(n):
    qvm = pq.QVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    
    prog = QProg()
    
    # Apply inverse QFT
    for i in range(n):
        # Apply inverse Hadamard (which is just Hadamard since H^2 = I)
        prog << pq.H(qubits[n-1-i])
        
        # Apply inverse controlled rotations
        for j in range(i):
            angle = -math.pi / (2 ** (i-j))
            prog << pq.CR(qubits[n-1-j], qubits[n-1-i], angle)
    
    # Reverse the order of qubits at the end for proper inverse QFT
    for i in range(n//2):
        prog << pq.SWAP(qubits[i], qubits[n-1-i])
    
    qvm.finalize()
    return prog
