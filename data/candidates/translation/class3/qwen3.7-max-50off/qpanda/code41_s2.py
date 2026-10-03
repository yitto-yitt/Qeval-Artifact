# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import PauliOperator

def compose_op():
    return PauliOperator("X0 Y2")
