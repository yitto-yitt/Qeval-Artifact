# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT


def apply_op_back():
    circ = QCircuit()
    circ << H(0)
    circ << CNOT(0, 1)
    circ << H(0)
    return circ
