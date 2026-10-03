# EVAL_META: task_id=145, framework=qpanda2, class=3
import pyqpanda as pq
from pyqpanda import *
import math

machine = pq.CPUQVM()
machine.init_qvm()

def qft_inverse(n):
    qubits = machine.qAlloc_many(n)
    prog = pq.QProg()
    
    # Apply inverse QFT
    # Inverse QFT is the reverse order of operations compared to QFT
    for i in range(n):
        # Apply Hadamard gate
        prog.insert(H(qubits[n-1-i]))
        
        # Apply controlled phase gates in reverse order
        for j in range(i):
            angle = -math.pi / (2 ** (i - j))
            prog.insert(CR(qubits[n-1-j], qubits[n-1-i], angle))
    
    # Reverse the order of qubits
    for i in range(n // 2):
        prog.insert(SWAP(qubits[i], qubits[n-1-i]))
    
    return prog, qubits

def finalize():
    machine.finalize()
