# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QOperator, PauliOperator


def compose_op():
    op = QOperator(np.eye(2**3))
    yx = QOperator(PauliOperator({"Y0 X1": 1.0}).to_matrix())
    return op.compose(yx, [0, 2])
