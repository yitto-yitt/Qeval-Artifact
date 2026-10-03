# EVAL_META: task_id=41, framework=qpanda, class=3
from pyqpanda3.core import *


def compose_op():
    return PauliOperator({"X0 Y2": 1.0})
