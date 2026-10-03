# EVAL_META: task_id=125, framework=qpanda, class=3
from pyqpanda3.core import *


def circ_to_gate(circ):
    to_gate = getattr(circ, "to_gate", None)
    if callable(to_gate):
        try:
            return to_gate()
        except TypeError:
            pass
    return circ
