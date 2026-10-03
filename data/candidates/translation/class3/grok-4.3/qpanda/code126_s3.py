# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, H, QProg, get_unitary


def calculate_phase_difference_fidelity():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubit = qvm.allocate_qubit()
    prog_a = QProg()
    prog_a << H(qubit)
    op_a = get_unitary(prog_a, qvm)
    op_b = np.exp(1j * 0.5) * op_a
    dim = op_a.shape[0]
    fidelity = (np.abs(np.trace(np.conj(op_a.T) @ op_b)) / dim) ** 2
    qvm.finalize()
    return float(fidelity)
