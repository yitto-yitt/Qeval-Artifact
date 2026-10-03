# EVAL_META: task_id=12, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, X

def get_unitary():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    U = np.zeros((4, 4), dtype=complex)
    perm = [0, 2, 1, 3]
    for col in range(4):
        prog = QProg()
        for i in range(2):
            if (col >> i) & 1:
                prog << X(q[i])
        prog << H(q[0])
        prog << CNOT(q[0], q[1])
        state = qvm.get_state_vector(prog)
        for row in range(4):
            U[row, col] = state[perm[row]]
    return U
