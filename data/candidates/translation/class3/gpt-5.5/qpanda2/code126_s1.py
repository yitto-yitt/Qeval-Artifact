# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

_h_gate = pq.H(q[0])
try:
    _h_matrix_raw = _h_gate.get_matrix()
except Exception:
    try:
        _h_matrix_raw = pq.get_matrix(_h_gate)
    except Exception:
        _prog = pq.QProg()
        _prog << _h_gate
        _h_matrix_raw = pq.get_matrix(_prog)

_H_MATRIX = np.array(_h_matrix_raw, dtype=complex)
if _H_MATRIX.size == 4:
    _H_MATRIX = _H_MATRIX.reshape((2, 2))


def calculate_phase_difference_fidelity():
    op_a = np.array(_H_MATRIX, dtype=complex)
    op_b = np.exp(1j * 0.5) * np.array(_H_MATRIX, dtype=complex)
    dim = op_a.shape[0]
    fidelity = abs(np.trace(np.conjugate(op_a.T) @ op_b)) ** 2 / (dim * dim)
    return float(np.real_if_close(fidelity))


machine.finalize()
