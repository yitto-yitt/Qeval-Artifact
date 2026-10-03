# EVAL_META: task_id=39, framework=qpanda2, class=2
from pyqpanda import *
def create_uniform_superposition(n):
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(n)
    prog = QProg()
    for q in qubits:
        prog << H(q)
    machine.directly_run(prog)
    state = machine.get_qstate()
    machine.finalize()
    return state
