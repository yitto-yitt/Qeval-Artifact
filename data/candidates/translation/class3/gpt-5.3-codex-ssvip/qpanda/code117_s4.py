# EVAL_META: task_id=117, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, matrix_decompose

def decompose_unitary(unitary):
    u = np.array(unitary, dtype=complex)
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    prog = QProg()
    prog << matrix_decompose(qubits, u.tolist())
    qvm.finalize()
    return prog
