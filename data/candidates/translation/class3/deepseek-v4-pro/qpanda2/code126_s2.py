# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def calculate_phase_difference_fidelity():
    prog_a = QProg()
    prog_a << H(q[0])
    unitary_a = np.asarray(get_matrix(prog_a))
    unitary_b = np.exp(1j * 0.5) * unitary_a
    d = unitary_a.shape[0]
    fidelity = np.abs(np.trace(np.conjugate(unitary_a.T) @ unitary_b)) ** 2 / d ** 2
    return float(fidelity)

machine.finalize()
