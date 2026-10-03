# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import init, QMachineType, QCircuit, X, RY, qAlloc_many

def tensor_circuits():
    init(QMachineType.CPU)
    q = qAlloc_many(3)

    top = QCircuit()
    top << X(q[2])

    bottom = QCircuit()
    bottom << RY(q[1], 0.2).control(q[0])

    tensored = QCircuit()
    tensored << bottom
    tensored << top
    return tensored
