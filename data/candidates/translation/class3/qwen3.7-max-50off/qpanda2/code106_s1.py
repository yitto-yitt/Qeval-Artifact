# EVAL_META: task_id=106, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def compose_cnot_dihedral():
    prog1 = QProg()
    prog1 << CNOT(q[0], q[1]) << T(q[0])
    
    prog2 = QProg()
    prog2 << CNOT(q[0], q[1]) << T(q[0]) << X(q[1])
    
    composed_prog = QProg()
    composed_prog << prog1 << prog2
    
    return composed_prog

machine.finalize()
