# EVAL_META: task_id=117, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

init(QMachineType.CPU)
q = qAlloc_many(2)

def decompose_unitary(unitary):
    mat = np.asarray(unitary, dtype=complex)
    return unitary_decomposer_nq(mat, q)

finalize()
