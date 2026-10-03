# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import QProg, QVec, Var, RX

def create_parametrized_gate():
    theta = Var("theta")
    qvec = QVec(1)
    prog = QProg()
    prog << RX(qvec[0], theta)
    return prog
