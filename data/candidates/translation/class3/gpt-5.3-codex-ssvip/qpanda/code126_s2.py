# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import H, matrix_decompose, CPUQVM, QProg


def calculate_phase_difference_fidelity():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)

    prog_a = QProg()
    prog_a << H(q[0])
    u_a = np.array(qvm.get_unitary(prog_a), dtype=complex)

    global_phase = np.exp(1j * 0.5)
    u_b = global_phase * u_a

    d = u_a.shape[0]
    fidelity = (abs(np.trace(np.conjugate(u_a.T) @ u_b)) ** 2) / (d ** 2)

    qvm.finalize()
    return float(np.real_if_close(fidelity))
