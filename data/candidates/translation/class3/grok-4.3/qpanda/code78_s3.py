# EVAL_META: task_id=78, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, H, CR
import math

def qft_no_swaps(num_qubits):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(num_qubits)
    circuit = QCircuit()
    for i in range(num_qubits - 1, -1, -1):
        for j in range(num_qubits - 1, i, -1):
            angle = -2 * math.pi / (2 ** (j - i))
            circuit << CR(qubits[j], qubits[i], angle)
        circuit << H(qubits[i])
    return circuit
