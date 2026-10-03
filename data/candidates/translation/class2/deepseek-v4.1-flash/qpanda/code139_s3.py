# EVAL_META: task_id=139, framework=qpanda, class=2
from pyqpanda3.core import DensityMatrix

def schmidt_test(data, qargs_B):
    return data.schmidt_decomposition(qargs_B)
