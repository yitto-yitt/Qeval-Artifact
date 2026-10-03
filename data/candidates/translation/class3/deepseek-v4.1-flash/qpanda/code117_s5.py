# EVAL_META: task_id=117, framework=qpanda, class=3
from pyqpanda3.core import decompose_unitary as pq_decompose_unitary

def decompose_unitary(unitary):
    return pq_decompose_unitary(unitary)
