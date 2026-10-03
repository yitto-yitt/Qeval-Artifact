# EVAL_META: task_id=78, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, H, CR

def qft_no_swaps(num_qubits):
    qubits = list(range(num_qubits))
    circuit = QCircuit()
    for j in range(num_qubits - 1, -1, -1):
        for k in range(num_qubits - 1, j, -1):
            angle = -np.pi / (2 ** (k - j))
            circuit << CR(qubits[k], qubits[j], -angle).dagger()
        circuit << H(qubits[j]).dagger()
    return circuit
