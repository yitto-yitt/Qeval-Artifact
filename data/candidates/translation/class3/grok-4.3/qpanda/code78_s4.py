# EVAL_META: task_id=78, framework=qpanda, class=3
from pyqpanda3.core import *
import math
def qft_no_swaps(num_qubits):
    prog = create_empty_qprog()
    q = qAlloc_many(num_qubits)
    for i in range(num_qubits - 1, -1, -1):
        for j in range(num_qubits - 1, i, -1):
            angle = -2 * math.pi / (2 ** (j - i))
            prog << CR(q[j], q[i], angle)
        prog << H(q[i])
    return prog
