# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import Var, QCircuit, RX, Qubit

def create_parametrized_gate():
    theta = Var("theta")
    q = Qubit()
    circ = QCircuit()
    circ << RX(q, theta)
    return circ
