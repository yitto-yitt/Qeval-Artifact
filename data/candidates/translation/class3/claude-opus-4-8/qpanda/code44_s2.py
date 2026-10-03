# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, X, RY

def tensor_circuits():
    tensored = QCircuit()
    tensored << X(0)
    tensored << RY(2, 0.2).control(1)
    prog = QProg()
    prog << tensored
    return prog
