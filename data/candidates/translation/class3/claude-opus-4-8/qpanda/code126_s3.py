# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import H, QCircuit, QProg


def calculate_phase_difference_fidelity():
    circ = QCircuit(1)
    circ << H(0)
    prog = QProg()
    prog << circ
    op_a = prog.matrix()
    op_a = np.array(op_a).reshape(2, 2)
    op_b = np.exp(1j * 0.5) * op_a

    d = op_a.shape[0]
    overlap = np.trace(op_a.conj().T @ op_b)
    fidelity = np.abs(overlap) ** 2 / d ** 2
    return fidelity
