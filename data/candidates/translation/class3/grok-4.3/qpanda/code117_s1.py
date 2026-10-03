# EVAL_META: task_id=117, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, matrix_decompose

def decompose_unitary(unitary):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    return matrix_decompose(q, unitary)
