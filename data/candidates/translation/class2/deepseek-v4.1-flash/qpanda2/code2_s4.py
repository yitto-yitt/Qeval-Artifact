# EVAL_META: task_id=2, framework=qpanda2, class=2
from math import sqrt
from pyqpanda import CPUQVM, QProg, H, CNOT


def create_bell_statevector():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    qvm.directly_run(prog)
    state = qvm.get_qstate()
    qvm.finalize()
    return state
