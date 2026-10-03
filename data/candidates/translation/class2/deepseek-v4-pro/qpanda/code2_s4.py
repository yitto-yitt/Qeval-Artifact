# EVAL_META: task_id=2, framework=qpanda, class=2
from pyqpanda3.core import (CNOT, H, QMachineType, QProg, finalize_qvm,
                            get_qstate, init_qvm, qalloc)


def create_bell_statevector():
    init_qvm(QMachineType.CPU)
    q = qalloc(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    state = get_qstate(prog, q)
    finalize_qvm()
    return state
