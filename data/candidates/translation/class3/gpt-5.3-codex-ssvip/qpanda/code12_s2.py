# EVAL_META: task_id=12, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, H, CNOT


def get_unitary():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])

    unitary = np.array(qvm.get_unitary(prog, q), dtype=complex)
    qvm.finalize()
    return unitary
