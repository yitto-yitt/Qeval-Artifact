# EVAL_META: task_id=90, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def create_custom_controlled():
    prog = QProg()
    prog << Toffoli(q[0], q[3], q[1])
    prog << H(q[2])
    return prog

machine.finalize()
