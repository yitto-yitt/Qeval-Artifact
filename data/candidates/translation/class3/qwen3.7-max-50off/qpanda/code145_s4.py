# EVAL_META: task_id=145, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QuantumMachine, QCircuit, H, SWAP, CR

def qft_inverse(n):
    qm = QuantumMachine()
    q = qm.qAlloc_many(n)
    circ = QCircuit()
    
    for i in range(n // 2):
        circ << SWAP(q[i], q[n - 1 - i])
        
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            angle = -np.pi / (2 ** (j - i))
            circ << CR(q[j], q[i], angle)
        circ << H(q[i])
        
    return circ
