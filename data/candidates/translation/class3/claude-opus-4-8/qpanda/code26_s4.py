# EVAL_META: task_id=26, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, H, CNOT, measure


def bell_dag():
    circ = QCircuit(3)
    circ << H(0)
    circ << CNOT(0, 1)
    prog = QProg()
    prog << circ
    prog << measure(0, 0)
    return prog
