# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, H


def calculate_phase_difference_fidelity():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)
    prog_a = QProg()
    prog_a << H(q[0])
    op_a = qvm.get_unitary(prog_a)
    op_b = np.exp(1j * 0.5) * op_a
    d = op_a.shape[0]
    fidelity = np.abs(np.trace(np.dot(np.conj(op_a.T), op_b)))**2 / d**2
    return fidelity
