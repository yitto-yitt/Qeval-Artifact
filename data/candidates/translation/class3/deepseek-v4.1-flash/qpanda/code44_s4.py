# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, X, CRY

def tensor_circuits():
    q0 = Qubit(0)
    q1 = Qubit(1)
    q2 = Qubit(2)
    circuit = QCircuit()
    circuit << CRY(q0, q1, 0.2)
    circuit << X(q2)
    return circuit
