# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, qAlloc_many, X, CRY, init, QMachineType

def tensor_circuits():
    init(QMachineType.CPU)
    q = qAlloc_many(3)
    circ = QCircuit()
    circ << CRY(q[0], q[1], 0.2)
    circ << X(q[2])
    return circ
