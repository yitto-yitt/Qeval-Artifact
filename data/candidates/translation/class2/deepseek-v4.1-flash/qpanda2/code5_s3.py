# EVAL_META: task_id=5, framework=qpanda2, class=2
from pyqpanda import QCircuit, X

def create_state_prep():
    circuit = QCircuit()
    circuit << X(1)
    return circuit
