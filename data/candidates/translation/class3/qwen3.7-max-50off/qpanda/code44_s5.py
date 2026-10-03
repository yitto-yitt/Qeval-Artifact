# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import QProg, Qubit, X, CRy

def tensor_circuits():
    q0 = Qubit(0)
    q1 = Qubit(1)
    q2 = Qubit(2)
    
    prog = QProg()
    prog << CRy(q0, q1, 0.2)
    prog << X(q2)
    return prog
