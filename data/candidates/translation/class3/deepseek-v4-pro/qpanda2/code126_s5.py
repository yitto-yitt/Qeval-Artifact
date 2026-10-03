# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def calculate_phase_difference_fidelity():
    prog = QProg()
    prog << H(q[0])

    matrix = np.asarray(get_matrix(prog), dtype=complex)
    op_b = np.exp(1j * 0.5) * matrix

    d = 2
    fidelity = np.abs(np.trace(matrix.conj().T @ op_b)) ** 2 / (d ** 2)
    return float(fidelity)

machine.finalize()
