# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QOperator


def compose_op():
    op = QOperator(np.eye(2**3, dtype=complex))
    yx = QOperator(np.kron(np.array([[0, -1j], [1j, 0]], dtype=complex),
                           np.array([[0, 1], [1, 0]], dtype=complex)))
    return op.compose(yx, qargs=[0, 2], front=True)
