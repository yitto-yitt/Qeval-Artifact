# EVAL_META: task_id=145, framework=qpanda2, class=3
from pyqpanda import *
import math

machine = CPUQVM()
machine.init_qvm()

def qft_inverse(n):
    q = machine.qAlloc_many(n)
    circuit = QCircuit()
    for i in range(n // 2):
        circuit << SWAP(q[i], q[n - 1 - i])
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            angle = -math.pi / (2 ** (j - i))
            circuit << CR(q[j], q[i], angle)
        circuit << H(q[i])
    return circuit
