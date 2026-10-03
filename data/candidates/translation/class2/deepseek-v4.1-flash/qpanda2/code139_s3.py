# EVAL_META: task_id=139, framework=qpanda2, class=2
from pyqpanda.quantum_info import schmidt_decomposition

def schmidt_test(data, qargs_B):
    return schmidt_decomposition(data, qargs_B)
