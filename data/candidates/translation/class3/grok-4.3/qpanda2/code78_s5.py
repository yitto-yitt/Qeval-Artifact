# EVAL_META: task_id=78, framework=qpanda2, class=3
from pyqpanda import *
import math
machine = CPUQVM()
machine.initQVM()
qubits = qAlloc_many(20)
def qft_no_swaps(num_qubits):
    circuit = QCircuit()
    qs = qubits[:num_qubits]
    for j in range(num_qubits - 1, -1, -1):
        for k in range(num_qubits - 1, j, -1):
            angle = -math.pi / (2 ** (k - j))
            circuit << CR(qs[k], qs[j], angle)
        circuit << H(qs[j])
    return circuit
machine.finalize()
