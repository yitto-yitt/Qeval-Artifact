# EVAL_META: task_id=2, framework=qpanda2, class=2
from pyqpanda import *


def create_bell_statevector():
    machine = init_quantum_machine(QMachineType.CPU)
    q = machine.qAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    machine.direct_run(prog)
    state = machine.get_qstate()
    machine.finalize()
    return state
