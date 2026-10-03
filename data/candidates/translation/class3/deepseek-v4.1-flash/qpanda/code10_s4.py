# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, X

def create_operator():
    circuit = QCircuit()
    circuit << X(0) << X(1)
    return circuit
