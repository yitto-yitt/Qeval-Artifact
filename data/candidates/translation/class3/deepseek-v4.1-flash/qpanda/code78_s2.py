# EVAL_META: task_id=78, framework=qpanda, class=3
import math
from pyqpanda3.core import QCircuit, H, CR

def qft_no_swaps(num_qubits):
    circuit = QCircuit()
    for j in range(num_qubits - 1, -1, -1):
        for k in range(num_qubits - 1, j, -1):
            angle = -math.pi / (2 ** (k - j))
            circuit << CR(k, j, angle)
        circuit << H(j)
    return circuit
