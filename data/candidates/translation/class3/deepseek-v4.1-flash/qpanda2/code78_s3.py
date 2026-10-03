# EVAL_META: task_id=78, framework=qpanda2, class=3
from pyqpanda import *
from math import pi

qvm = CPUQVM()
qvm.init_qvm()
global_qubits = qvm.qAlloc_many(1000)

def qft_no_swaps(num_qubits):
    qubits = global_qubits[:num_qubits]
    circuit = QCircuit()
    for i in reversed(range(num_qubits)):
        for j in reversed(range(i + 1, num_qubits)):
            circuit << CR(qubits[j], qubits[i], -pi / (2 ** (j - i)))
        circuit << H(qubits[i])
    return circuit
