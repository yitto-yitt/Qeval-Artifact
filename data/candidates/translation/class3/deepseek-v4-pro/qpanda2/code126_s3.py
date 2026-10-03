# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.initQVM()
q = machine.qAlloc_many(1)

def calculate_phase_difference_fidelity():
    prog_a = QProg()
    prog_a << H(q[0])
    
    op_a = np.asarray(get_matrix(prog_a, q))
    op_b = np.exp(1j * 0.5) * op_a
    
    d = op_a.shape[0]
    fidelity = np.abs(np.trace(op_a.conj().T @ op_b)) ** 2 / d ** 2
    return float(fidelity)

machine.finalize()
