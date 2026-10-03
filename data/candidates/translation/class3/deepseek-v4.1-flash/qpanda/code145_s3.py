# EVAL_META: task_id=145, framework=qpanda, class=3
import math
from pyqpanda3.core import QCircuit, Qubit, H, CP, SWAP

def qft_inverse(n):
    circuit = QCircuit()
    qubits = [Qubit(i) for i in range(n)]
    for i in range(n // 2):
        circuit << SWAP(qubits[i], qubits[n - i - 1])
    for j in reversed(range(n)):
        for k in reversed(range(j + 1, n)):
            angle = -math.pi / (2 ** (k - j))
            circuit << CP(qubits[k], qubits[j], angle)
        circuit << H(qubits[j])
    return circuit
