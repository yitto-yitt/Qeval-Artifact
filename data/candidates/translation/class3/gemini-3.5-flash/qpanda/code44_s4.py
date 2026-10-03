# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, X, CRY

def tensor_circuits():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    prog = QProg()
    prog << X(q[0]) << CRY(q[1], q[2], 0.2)
    return prog
