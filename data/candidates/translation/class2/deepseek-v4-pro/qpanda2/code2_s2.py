# EVAL_META: task_id=2, framework=qpanda2, class=2
from pyqpanda import *


def create_bell_statevector():
    init_quantum_machine(QMachineType.CPU)
    q = qAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    directly_run(prog)
    state = list(get_qstate())
    finalize_quantum_machine()
    return state
