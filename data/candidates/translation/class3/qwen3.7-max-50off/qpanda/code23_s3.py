# EVAL_META: task_id=23, framework=qpanda, class=3
from pyqpanda3.core import QProg, X, QMachine

def dj_constant_oracle():
    qm = QMachine()
    q = qm.alloc_qubits(3)
    prog = QProg()
    prog << X(q[2])
    return prog
