# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import Operator, Pauli


def compose_op():
    op = Operator(np.eye(2**3))
    yx = Operator(Pauli("YX"))
    return op.compose(yx, qargs=[0, 2], front=True)
