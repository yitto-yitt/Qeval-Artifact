# EVAL_META: task_id=41, framework=qpanda, class=3
from pyqpanda3.core import PauliOperator


def compose_op():
    return PauliOperator({"Y2 X0": 1.0})
