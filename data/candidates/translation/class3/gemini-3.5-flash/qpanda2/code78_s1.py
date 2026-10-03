# EVAL_META: task_id=78, framework=qpanda2, class=3
import math
from pyqpanda import CPUQVM, QCircuit, H, CU1

machine = CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(100)

def qft_no_swaps(num_qubits):
    circuit = QCircuit()
    qubits = global_qubits[:num_qubits]
    for i in range(num_qubits):
        for j in range(i):
            theta = -math.pi / (2 ** (i - j))
            circuit << CU1(qubits[i], qubits[j], theta)
        circuit << H(qubits[i])
    return circuit

machine.finalize()
