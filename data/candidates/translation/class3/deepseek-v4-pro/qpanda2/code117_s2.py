# EVAL_META: task_id=117, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def decompose_unitary(unitary):
    mat = np.array(unitary, dtype=complex)
    return unitary_decomposer(q, mat)

machine.finalize()
