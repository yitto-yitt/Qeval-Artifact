# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def calculate_phase_difference_fidelity():
    prog_a = QProg()
    prog_a << H(q[0])
    
    mat_a_flat = get_matrix(prog_a)
    mat_a = np.array(mat_a_flat).reshape(2, 2)
    
    mat_b = np.exp(1j * 0.5) * mat_a
    
    d = 2
    fidelity = np.abs(np.trace(np.dot(mat_a.conj().T, mat_b)))**2 / (d**2)
    return fidelity

machine.finalize()
