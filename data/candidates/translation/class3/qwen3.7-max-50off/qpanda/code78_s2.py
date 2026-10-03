# EVAL_META: task_id=78, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QuantumMachine, QCircuit, H, CR

def qft_no_swaps(num_qubits):
    qm = QuantumMachine()
    q = qm.qAlloc_many(num_qubits)
    circ = QCircuit()
    
    for i in range(num_qubits - 1, -1, -1):
        for j in range(num_qubits - 1, i, -1):
            angle = -np.pi / (2 ** (j - i))
            circ << CR(angle, q[j], q[i])
        circ << H(q[i])
        
    return circ
