# EVAL_META: task_id=2, framework=qpanda2, class=2
from pyqpanda import *


def create_bell_statevector():
    init(QMachineType.CPU)
    q = qAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    directly_run(prog)
    state = get_qstate()
    finalize()
    return state
