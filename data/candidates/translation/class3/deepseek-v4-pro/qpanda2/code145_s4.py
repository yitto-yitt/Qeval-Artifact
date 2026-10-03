# EVAL_META: task_id=145, framework=qpanda2, class=3
import math
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()

def qft_inverse(n):
    q = machine.qAlloc_many(n)
    circuit = QCircuit()

    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            circuit << CP(q[j], q[i], -math.pi / (1 << (j - i)))
        circuit << H(q[i])

    return circuit

machine.finalize()
