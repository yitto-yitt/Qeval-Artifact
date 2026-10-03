# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, H

try:
    from pyqpanda3.core import get_matrix as _core_get_matrix
except ImportError:
    _core_get_matrix = None


def calculate_phase_difference_fidelity():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)

    prog = QProg()
    prog << H(q[0])

    try:
        op_a = np.asarray(qvm.get_matrix(prog, q), dtype=complex)
    except Exception:
        if _core_get_matrix is not None:
            op_a = np.asarray(_core_get_matrix(prog, qvm, q), dtype=complex)
        else:
            raise

    op_b = np.exp(1j * 0.5) * op_a
    dim = op_a.shape[0]
    return float(np.abs(np.trace(op_a.conj().T @ op_b)) ** 2 / (dim * dim))
