# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, H


def calculate_phase_difference_fidelity():
    qvm = CPUQVM()
    qvm.init()
    qubits = qvm.qAllocMany(1)

    h_gate = H(qubits[0])
    op_a = np.asarray(h_gate.get_matrix(), dtype=complex)
    op_b = np.exp(1j * 0.5) * op_a

    dim = op_a.shape[0]
    fidelity = np.abs(np.trace(op_a.conj().T @ op_b)) ** 2 / (dim ** 2)
    return float(fidelity)
