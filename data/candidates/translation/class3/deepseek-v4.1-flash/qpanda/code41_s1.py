# EVAL_META: task_id=41, framework=qpanda, class=3
from pyqpanda3.core import QProg, Qubit, X, Y, QOperator


def compose_op():
    prog = QProg()
    q = [Qubit(i) for i in range(3)]
    prog << Y(q[0])
    prog << X(q[2])
    return QOperator(prog)
