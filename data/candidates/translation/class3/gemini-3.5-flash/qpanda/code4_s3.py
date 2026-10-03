# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda3.core import *

def create_unitary_from_matrix():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    
    matrix = [
        0+0j, 0+0j, 0+0j, 1+0j,
        0+0j, 0+0j, 1+0j, 0+0j,
        1+0j, 0+0j, 0+0j, 0+0j,
        0+0j, 1+0j, 0+0j, 0+0j
    ]
    
    gate = matrix_gate(q, matrix)
    prog = QProg()
    prog << gate
    return prog
