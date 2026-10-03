# EVAL_META: task_id=125, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QGate


def circ_to_gate(circ):
    circ_gate = QCircuit()
    circ_gate << circ
    return circ_gate
