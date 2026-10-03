# EVAL_META: task_id=78, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit

def qft_no_swaps(num_qubits):
    circuit = QCircuit()
    for j in range(num_qubits - 1, -1, -1):
        for k in range(num_qubits - 1, j, -1):
            circuit.cp(-np.pi / (2 ** (k - j)), k, j)
        circuit.h(j)
    return circuit
