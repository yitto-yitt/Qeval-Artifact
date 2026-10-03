# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda3.core import QProg, CNOT, X

def create_unitary_from_matrix():
    circuit = QProg()
    circuit << CNOT(1, 0)
    circuit << X(1)
    return circuit
