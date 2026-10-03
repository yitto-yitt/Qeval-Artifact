# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

qvm = CPUQVM()
qvm.init_qvm()
qubits = qvm.qAlloc_many(1)


def calculate_phase_difference_fidelity():
    prog = QProg()
    prog << H(0)
    U = get_unitary(prog)
    V = np.exp(1j * 0.5) * U
    d = U.shape[0]
    fidelity = np.abs(np.trace(U.conj().T @ V)) ** 2 / d ** 2
    return fidelity


qvm.finalize()
