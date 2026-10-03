# EVAL_META: task_id=5, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, Qubit, X

def create_state_prep():
    q = Qubit(2)
    circ = QCircuit()
    circ << X(q[0])
    return circ
