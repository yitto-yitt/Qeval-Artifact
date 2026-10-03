# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QProg, Qubit, QGate, get_unitary

def compose_op():
    prog = QProg()
    q = Qubit(3)
    prog << QGate.Y(q[0]) << QGate.X(q[2])
    return get_unitary(prog)
