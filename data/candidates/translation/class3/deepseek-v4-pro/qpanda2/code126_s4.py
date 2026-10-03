# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QProg, H, get_matrix

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def calculate_phase_difference_fidelity():
    prog = QProg()
    prog << H(q[0])
    op_a = np.array(get_matrix(prog))
    op_b = np.exp(1j * 0.5) * op_a
    dim = op_a.shape[0]
    fidelity = np.abs(np.trace(np.conj(op_a).T @ op_b)) ** 2 / (dim * dim)
    return float(fidelity)

machine.finalize()
