# EVAL_META: task_id=145, framework=qpanda2, class=3
import pyqpanda as pq
from pyqpanda import *
import math

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)  # Assuming max 10 qubits for safety

def qft_inverse(n):
    qvm = machine
    q = qubits[:n]
    
    # Apply inverse QFT
    # Inverse QFT is the reverse of QFT: 
    # 1. Reverse order of operations
    # 2. Change phase angles to negative
    
    # First apply Hadamard gates in reverse order
    for i in range(n-1, -1, -1):
        H(q[i])
        
        # Apply controlled phase gates in reverse order
        for j in range(i-1, -1, -1):
            angle = -math.pi / (2 ** (i-j))
            CR(q[j], q[i], angle)
    
    # Reverse the qubit order to complete inverse QFT
    for i in range(n // 2):
        SWAP(q[i], q[n-1-i])
    
    return q

# Manual cleanup
machine.finalize()
