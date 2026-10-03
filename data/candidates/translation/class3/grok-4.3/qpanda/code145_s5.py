# EVAL_META: task_id=145, framework=qpanda, class=3
from pyqpanda3.core import *
import math
def qft_inverse(n):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n)
    circ = QCircuit()
    for i in range(n):
        for j in range(i):
            circ << CR(q[j], q[i], -math.pi / 2**(i - j))
        circ << H(q[i])
    for i in range(n // 2):
        circ << SWAP(q[i], q[n - 1 - i])
    return circ
