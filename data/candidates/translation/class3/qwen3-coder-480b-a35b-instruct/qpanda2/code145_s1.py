# EVAL_META: task_id=145, framework=qpanda2, class=3
import pyqpanda as pq
from pyqpanda import *
import math

machine = pq.CPUQVM()
machine.init_qvm()

def qft_inverse(n):
    qubits = machine.qAlloc_many(n)
    prog = pq.QProg()
    
    # Apply inverse QFT: reverse the order of operations in regular QFT
    for i in range(n):
        # Apply inverse Hadamard (which is the same as regular Hadamard)
        prog << H(qubits[n-1-i])
        
        # Apply inverse controlled rotations
        for j in range(i+1, n):
            angle = -math.pi / (2**(j-i))
            prog << CR(qubits[n-1-j], qubits[n-1-i], angle)
    
    # Reverse the order of qubits to complete the inverse QFT
    for i in range(n//2):
        prog << SWAP(qubits[i], qubits[n-1-i])
    
    return prog, qubits

def finalize():
    machine.finalize()
