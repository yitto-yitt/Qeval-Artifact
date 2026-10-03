# EVAL_META: task_id=145, framework=qpanda2, class=3
import math
from pyqpanda import *

# Global QVM
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(24)

def qft_inverse(n):
    circuit = QCircuit()
    for i in range(n // 2):
        circuit << SWAP(q[i], q[n - 1 - i])
    for i in range(n):
        for j in range(i):
            angle = -math.pi / (1 << (i - j))
            circuit << U1(q[i], angle).control([q[j]])
        circuit << H(q[i])
    return circuit

machine.finalize()
