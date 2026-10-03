# EVAL_META: task_id=5, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, X, I


def create_state_prep():
    circuit = QCircuit()
    circuit << X(0) << I(1)
    return circuit
