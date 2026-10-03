# EVAL_META: task_id=78, framework=qpanda2, class=3
import math
from pyqpanda import *

qvm = CPUQVM()
qvm.init_qvm()

def qft_no_swaps(num_qubits):
    qubits = qvm.qAlloc_many(num_qubits)
    circuit = QCircuit()
    for j in range(num_qubits - 1, -1, -1):
        for k in range(num_qubits - 1, j, -1):
            circuit << CP(qubits[j], qubits[k], -math.pi / (2 ** (k - j)))
        circuit << H(qubits[j])
    return circuit

qvm.finalize()
