# EVAL_META: task_id=78, framework=qpanda2, class=3
from pyqpanda import *
import math

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)

def qft_no_swaps(num_qubits):
    circuit = QCircuit()
    for i in range(num_qubits - 1, -1, -1):
        for j in range(num_qubits - 1, i, -1):
            angle = -math.pi / (2 ** (j - i))
            circuit << CR(qubits[j], qubits[i], angle)
        circuit << H(qubits[i])
    return circuit
