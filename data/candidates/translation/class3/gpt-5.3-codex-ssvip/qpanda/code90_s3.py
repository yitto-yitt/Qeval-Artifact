# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import *

def create_custom_controlled():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(4)

    base_prog = QProg()
    base_prog << X(q[0]) << H(q[1])

    controlled_prog = QProg()
    controlled_prog << X(q[1]).control([q[0], q[3]])
    controlled_prog << H(q[2]).control([q[0], q[3]])

    prog = QProg()
    prog << controlled_prog
    return prog
