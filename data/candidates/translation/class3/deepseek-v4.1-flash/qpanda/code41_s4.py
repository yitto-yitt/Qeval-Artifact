# EVAL_META: task_id=41, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, X, Y, QOperator

def compose_op():
    cir = QCircuit()
    cir << X(0) << Y(2)
    return QOperator(cir)
