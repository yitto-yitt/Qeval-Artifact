# EVAL_META: task_id=145, framework=qpanda, class=3
import pyqpanda3 as pq
from pyqpanda3 import *
import numpy as np

def qft_inverse(n):
    qvm = pq.QVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(n)
    
    # Implement inverse QFT manually since there's no direct inverse QFT in pyqpanda3
    # Inverse QFT is the Hermitian conjugate of QFT
    # Reverse the order of operations in QFT and take conjugate transpose
    
    # Create the circuit
    prog = pq.QProg()
    
    # Apply inverse QFT: reverse the order of gates compared to normal QFT
    for i in range(n):
        # Apply Hadamard gate to the current qubit
        prog.insert(pq.H(q[n-1-i]))
        
        # Apply controlled phase shift gates in reverse order
        for j in range(i):
            # The angle for the controlled rotation is -pi/2^(i-j)
            angle = -np.pi / (2 ** (i - j))
            prog.insert(pq.CR(q[n-1-j], q[n-1-i], angle))
    
    # Apply SWAP gates to reverse the order of qubits at the end
    for i in range(n // 2):
        prog.insert(pq.SWAP(q[i], q[n-1-i]))
    
    qvm.finalize()
    return prog
