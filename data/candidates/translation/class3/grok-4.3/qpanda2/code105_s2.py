# EVAL_META: task_id=105, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def initialize_cnot_dihedral():
    prog = QProg()
    prog << CNOT(q[0], q[1]) << T(q[0])
    return prog

machine.finalize()
