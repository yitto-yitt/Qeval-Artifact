# EVAL_META: task_id=139, framework=qpanda, class=2
from pyqpanda3.core import schmidt_decomposition

def schmidt_test(data, qargs_B):
    return schmidt_decomposition(data, qargs_B)
