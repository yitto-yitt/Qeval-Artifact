# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, H

def calculate_phase_difference_fidelity():
    qvm = CPUQVM()
    prog = QProg()
    prog << H(0)
    unitary_a = np.array(qvm.get_unitary(prog))
    unitary_b = np.exp(1j * 0.5) * unitary_a
    d = unitary_a.shape[0]
    fidelity = np.abs(np.trace(unitary_a.conj().T @ unitary_b)) ** 2 / (d ** 2)
    return float(fidelity)
