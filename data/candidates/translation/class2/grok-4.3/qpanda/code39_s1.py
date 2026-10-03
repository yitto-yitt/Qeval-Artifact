# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, create_empty_qprog, H

def create_uniform_superposition(n):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n)
    prog = create_empty_qprog()
    for i in range(n):
        prog << H(q[i])
    machine.directly_run(prog)
    state = machine.get_qstate()
    machine.finalize()
    return state
