# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QOperator, PauliOperator

def compose_op():
    identity = QOperator(np.eye(2 ** 3))
    yx = QOperator(PauliOperator("Y0 X1").to_matrix(2))
    return identity.compose(yx, qargs=[0, 2], front=True)
