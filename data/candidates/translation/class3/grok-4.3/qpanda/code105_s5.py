# EVAL_META: task_id=105, framework=qpanda, class=3
from pyqpanda3.core import *

def initialize_cnot_dihedral():
    q = qAlloc_many(2)
    prog = QProg()
    prog << CX(q[0], q[1]) << T(q[0])
    return prog
