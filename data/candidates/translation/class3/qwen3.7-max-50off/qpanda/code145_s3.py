# EVAL_META: task_id=145, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, Qubit, H, SWAP, CPhase

def qft_inverse(n):
    qubits = [Qubit() for _ in range(n)]
    circ = QCircuit()
    
    for i in range(n // 2):
        circ << SWAP(qubits[i], qubits[n - 1 - i])
        
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            angle = -np.pi / (2 ** (j - i))
            circ << CPhase(qubits[j], qubits[i], angle)
        circ << H(qubits[i])
        
    return circ
