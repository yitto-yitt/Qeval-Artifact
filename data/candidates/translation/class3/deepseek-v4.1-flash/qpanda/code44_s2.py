# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, X, CRY

def tensor_circuits():
    q = [Qubit(i) for i in range(3)]
    circuit = QCircuit()
    circuit << CRY(q[0], q[1], 0.2)
    circuit << X(q[2])
    return circuit
