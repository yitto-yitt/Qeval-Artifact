# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

# Global QVM
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)


def calculate_phase_difference_fidelity():
    prog = QProg()
    prog << H(q[0])

    mat_list = get_matrix(prog)
    op_a = np.array(mat_list).reshape(2, 2)
    op_b = np.exp(1j * 0.5) * op_a

    d = op_a.shape[0]
    trace_val = np.trace(np.dot(op_a.conj().T, op_b))
    fidelity = (np.abs(trace_val) ** 2) / (d**2)

    return fidelity


machine.finalize()
