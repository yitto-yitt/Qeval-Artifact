# EVAL_META: task_id=26, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, H, CNOT, measure


def bell_dag():
    circ = QProg()
    circ << H(0)
    circ << CNOT(0, 1)
    circ << measure(0, 0)
    return circ
