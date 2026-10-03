# EVAL_META: task_id=145, framework=qpanda2, class=3
import math
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(20)

def qft_inverse(n):
    q = qubits[:n]
    circuit = QCircuit()
    for i in range(n // 2):
        circuit << SWAP(q[i], q[n - 1 - i])
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            angle = -math.pi / (2 ** (j - i))
            circuit << CR(q[i], q[j], angle)
        circuit << H(q[i])
    return circuit

machine.finalize()
