# EVAL_META: task_id=125, framework=qpanda, class=3
from pyqpanda3.core import *


def circ_to_gate(circ):
    if hasattr(circ, "to_gate"):
        return circ.to_gate()
    return circ
