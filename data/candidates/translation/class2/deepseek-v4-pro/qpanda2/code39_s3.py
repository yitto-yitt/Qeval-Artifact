# EVAL_META: task_id=39, framework=qpanda2, class=2
from pyqpanda import *

def create_uniform_superposition(n):
    if n == 0:
        return [1+0j]

    machine = CPUQVM()
    machine.init()
    qubits = machine.qAlloc_many(n)

    prog = QProg()
    for i in range(n):
        prog << H(qubits[i])

    if hasattr(machine, 'directlyRun'):
        machine.directlyRun(prog)
    else:
        machine.directly_run(prog)

    if hasattr(machine, 'getQState'):
        state = machine.getQState()
    else:
        state = machine.get_qstate()

    if hasattr(machine, 'finalize'):
        machine.finalize()

    return state
