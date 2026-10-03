# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, H, X


def calculate_phase_difference_fidelity():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)

    prog0 = QProg()
    prog0 << H(q[0])
    qvm.run(prog0)
    state0 = qvm.get_qstate()

    prog1 = QProg()
    prog1 << X(q[0])
    prog1 << H(q[0])
    qvm.run(prog1)
    state1 = qvm.get_qstate()

    U = np.array([state0, state1]).T
    V = np.exp(1j * 0.5) * U

    d = U.shape[0]
    tr = np.trace(U.conj().T @ V)
    fidelity = np.abs(tr) ** 2 / (d ** 2)
    return fidelity
