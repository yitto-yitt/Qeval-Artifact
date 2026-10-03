# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, X

def create_operator():
    circ = QCircuit(2)
    circ << X(0)
    circ << X(1)
    prog = QProg()
    prog << circ
    return prog
