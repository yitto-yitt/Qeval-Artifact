# EVAL_META: task_id=89, framework=qpanda, class=3
from pyqpanda3.core import *

def create_controlled_hgate():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    prog = QProg()
    ch_gate = H(q[2]).control([q[0], q[1]])
    prog.insert(ch_gate)
    return prog
