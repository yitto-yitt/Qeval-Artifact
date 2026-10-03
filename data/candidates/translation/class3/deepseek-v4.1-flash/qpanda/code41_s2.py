# EVAL_META: task_id=41, framework=qpanda, class=3
from pyqpanda3.core import QOperator, QCircuit, Y, X


def compose_op():
    circ = QCircuit()
    circ << Y(0) << X(2)
    return QOperator(circ)
