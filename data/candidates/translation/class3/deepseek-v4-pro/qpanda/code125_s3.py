# EVAL_META: task_id=125, framework=qpanda, class=3
from pyqpanda3.core import QGate


def circ_to_gate(circ):
    return QGate(circ)
