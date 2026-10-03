# EVAL_META: task_id=126, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

qvm = CPUQVM()
qvm.init_qvm()
qubits = qvm.qAlloc_many(1)

def calculate_phase_difference_fidelity():
    prog = QProg()
    prog << H(qubits[0])
    mat_a = qvm.unitary(prog)
    mat_b = np.exp(1j * 0.5) * mat_a
    d = mat_a.shape[0]
    overlap = np.trace(mat_a.conj().T @ mat_b)
    fidelity = np.abs(overlap)**2 / (d**2)
    return fidelity
