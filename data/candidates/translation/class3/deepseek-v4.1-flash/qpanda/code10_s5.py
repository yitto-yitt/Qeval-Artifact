# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, qubit, X

def create_operator():
    q = qubit(2)
    circuit = QCircuit()
    circuit << X(q[0]) << X(q[1])
    return circuit
