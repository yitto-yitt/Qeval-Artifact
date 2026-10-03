# EVAL_META: task_id=5, framework=qpanda2, class=2
from pyqpanda import QCircuit, X, Qubit

def create_state_prep():
    circuit = QCircuit()
    q0 = Qubit(0)
    circuit << X(q0)
    return circuit
