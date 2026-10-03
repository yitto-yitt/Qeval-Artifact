# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()

def calculate_phase_difference_fidelity():
    prog_a = QProg()
    qubits = machine.qAlloc_many(1)
    prog_a << H(qubits[0])
    matrix_a = get_unitary(prog_a)
    
    matrix_b = np.exp(1j * 0.5) * matrix_a
    
    fidelity = np.abs(np.trace(np.dot(matrix_a.conj().T, matrix_b))) / matrix_a.shape[0]
    
    return fidelity

machine.finalize()
