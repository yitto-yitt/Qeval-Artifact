# EVAL_META: task_id=78, framework=qpanda2, class=3
from pyqpanda import *
import math
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)
def qft_no_swaps(num_qubits):
    prog = QProg()
    q = qubits[:num_qubits]
    for i in range(num_qubits - 1, -1, -1):
        for j in range(num_qubits - 1, i, -1):
            prog << CR(q[j], q[i], -math.pi / 2 ** (j - i))
        prog << H(q[i])
    return prog
machine.finalize()
