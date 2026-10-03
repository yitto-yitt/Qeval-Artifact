# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, H


def calculate_phase_difference_fidelity():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc()
    prog = QProg()
    prog << H(q)
    U = qvm.get_unitary(prog)
    V = np.exp(1j * 0.5) * U
    fidelity = np.abs(np.trace(U.conj().T @ V)) ** 2 / (U.shape[0] ** 2)
    qvm.finalize()
    return fidelity
