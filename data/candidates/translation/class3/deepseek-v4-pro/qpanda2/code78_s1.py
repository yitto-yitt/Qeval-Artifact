# EVAL_META: task_id=78, framework=qpanda2, class=3
from pyqpanda import *
import math

machine = CPUQVM()
machine.init_qvm()

def qft_no_swaps(num_qubits):
    q = machine.qAlloc_many(num_qubits)
    circuit = QCircuit()
    for i in range(num_qubits - 1, -1, -1):
        for j in range(num_qubits - 1, i, -1):
            circuit << CP(q[j], q[i], -math.pi / (2 ** (j - i)))
        circuit << H(q[i])
    return circuit

machine.finalize()
