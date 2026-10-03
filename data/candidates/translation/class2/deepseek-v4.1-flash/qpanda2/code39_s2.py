# EVAL_META: task_id=39, framework=qpanda2, class=2
from pyqpanda import *

def create_uniform_superposition(n):
    machine = init_quantum_machine(QMachineType.CPU)
    q = machine.qAlloc_many(n)
    prog = QProg()
    for i in range(n):
        prog << H(q[i])
    machine.directly_run(prog)
    state = machine.get_qstate()
    machine.finalize()
    return state
