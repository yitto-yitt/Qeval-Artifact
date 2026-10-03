# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

qvm = CPUQVM()
qvm.init_qvm()
q = qvm.qAlloc_many(1)

_h_gate = H(q[0])
try:
    _H_MATRIX = np.array(_h_gate.get_matrix(), dtype=complex)
except AttributeError:
    _prog = QProg()
    _prog << _h_gate
    _H_MATRIX = np.array(get_matrix(_prog), dtype=complex)

if _H_MATRIX.size != 4:
    raise ValueError("Unexpected H matrix size")
_H_MATRIX = _H_MATRIX.reshape(2, 2)


def calculate_phase_difference_fidelity():
    mat_a = _H_MATRIX
    mat_b = np.exp(1j * 0.5) * mat_a
    dim = mat_a.shape[0]
    fidelity = np.abs(np.trace(mat_a.conj().T @ mat_b)) ** 2 / (dim * dim)
    return float(fidelity)


qvm.finalize()
