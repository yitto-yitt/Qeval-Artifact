# EVAL_META: task_id=126, framework=qpanda2, class=3
import atexit
import numpy as np
from pyqpanda import CPUQVM, H

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)
atexit.register(machine.finalize)


def calculate_phase_difference_fidelity():
    op_a = np.asarray(H(q[0]).get_matrix(), dtype=complex)
    if op_a.ndim == 1:
        dim = int(round(np.sqrt(op_a.size)))
        op_a = op_a.reshape((dim, dim))

    op_b = np.exp(1j * 0.5) * op_a
    dim = op_a.shape[0]
    fidelity = abs(np.trace(op_a.conj().T @ op_b)) ** 2 / (dim * dim)
    return float(np.real_if_close(fidelity))
