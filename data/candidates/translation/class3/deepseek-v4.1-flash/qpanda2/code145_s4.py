# EVAL_META: task_id=145, framework=qpanda2, class=3
from pyqpanda import *
import math

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(100)

def qft_inverse(n):
    circuit = QCircuit()
    q = qubits[:n]
    for i in range(n // 2):
        circuit << SWAP(q[i], q[n - 1 - i])
    for j in range(n - 1, -1, -1):
        for k in range(n - 1, j, -1):
            angle = -math.pi / (2 ** (k - j))
            circuit << CR(q[k], q[j], angle)
        circuit << H(q[j])
    return circuit
