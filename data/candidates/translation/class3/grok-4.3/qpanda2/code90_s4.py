# EVAL_META: task_id=90, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.initQVM()
q = machine.qAlloc_many(4)

def create_custom_controlled():
    prog = QProg()
    prog << X(q[1]).control(q[0]).control(q[3])
    prog << H(q[2]).control(q[0]).control(q[3])
    return prog

machine.finalize()
