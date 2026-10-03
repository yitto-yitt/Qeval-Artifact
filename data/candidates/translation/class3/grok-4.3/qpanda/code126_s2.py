# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, H, get_unitary


def calculate_phase_difference_fidelity():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)
    prog_a = QProg()
    prog_a << H(q[0])
    u_a = get_unitary(machine, prog_a)
    u_b = np.exp(1j * 0.5) * u_a
    d = u_a.shape[0]
    fidelity = np.abs(np.trace(np.conj(u_a).T @ u_b)) ** 2 / d ** 2
    machine.finalize()
    return fidelity
