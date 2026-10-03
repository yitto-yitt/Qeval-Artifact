# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda3.core import *

def create_unitary_from_matrix():
    matrix = [
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0]
    ]
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    prog = QProg()
    prog.insert(QOracle(q, matrix))
    return prog
