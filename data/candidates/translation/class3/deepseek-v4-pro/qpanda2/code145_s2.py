# EVAL_META: task_id=145, framework=qpanda2, class=3
import math
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
_allocated_qubits = []

def qft_inverse(n):
    if n <= 0:
        return QCircuit()
    q = machine.qAlloc_many(n)
    _allocated_qubits.extend(list(q))
    circuit = QCircuit()

    for i in range(n // 2):
        circuit << SWAP(q[i], q[n - 1 - i])

    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            circuit << CP(q[j], q[i], -math.pi / (2 ** (j - i)))
        circuit << H(q[i])

    return circuit

machine.finalize()
