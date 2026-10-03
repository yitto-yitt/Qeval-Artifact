# EVAL_META: task_id=125, framework=qpanda, class=3
from pyqpanda import *


def circ_to_gate(circ):
    # Convert the pyQPanda circuit to a QGate
    circ_gate = circ.get_qgate()
    return circ_gate
