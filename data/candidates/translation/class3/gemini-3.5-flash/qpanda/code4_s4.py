# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, CNOT, X, qAlloc_many

def create_unitary_from_matrix():
    q = qAlloc_many(2)
    circuit = QCircuit()
    circuit.insert(CNOT(q[1], q[0]))
    circuit.insert(X(q[1]))
    return circuit
