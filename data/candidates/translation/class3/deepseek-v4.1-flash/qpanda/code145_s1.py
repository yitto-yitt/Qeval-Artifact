# EVAL_META: task_id=145, framework=qpanda, class=3
import math
from pyqpanda3.core import QCircuit, Qubit, H, CP, SWAP

def qft_inverse(n):
    circuit = QCircuit()
    qubits = [Qubit(i) for i in range(n)]
    for i in range(n // 2):
        circuit << SWAP(qubits[i], qubits[n - 1 - i])
    for j in range(n - 1, -1, -1):
        for k in range(n - 1, j, -1):
            theta = -math.pi / (2 ** (k - j))
            circuit << CP(qubits[k], qubits[j], theta)
        circuit << H(qubits[j])
    return circuit
