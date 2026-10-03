# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import *

def create_uniform_superposition(n):
    init_qvm()
    q = qalloc(n)
    prog = QProg()
    for qubit in q:
        prog << H(qubit)
    state = get_qstate(prog, q)
    final_qvm()
    return state
