# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg, H

def create_uniform_superposition(n):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(n)
    prog = QProg()
    for i in range(n):
        prog << H(q[i])
    qvm.run(prog)
    return qvm.get_qstate()
