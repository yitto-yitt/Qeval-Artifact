# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, X, RY

def tensor_circuits():
    top = QCircuit(1)
    top << X(0)

    bottom = QCircuit(2)
    bottom << RY(2, 0.2).control([1])

    tensored = QCircuit(3)
    tensored << top
    shifted = bottom.remap({0: 1, 1: 2})
    tensored << shifted

    return tensored
