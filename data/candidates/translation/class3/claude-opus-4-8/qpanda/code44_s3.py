# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, X, RY

def tensor_circuits():
    top = QCircuit(1)
    top << X(0)

    bottom = QCircuit(2)
    bottom << RY(2, 0.2).control(1)

    tensored = QCircuit(3)
    tensored << top

    shifted = QCircuit(3)
    shifted << RY(2 + 1, 0.2).control(1 + 1)
    tensored << shifted

    return tensored
