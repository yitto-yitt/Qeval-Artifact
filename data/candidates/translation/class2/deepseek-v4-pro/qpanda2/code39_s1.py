# EVAL_META: task_id=39, framework=qpanda2, class=2
from pyqpanda import *

_initialized = False

def create_uniform_superposition(n):
    global _initialized
    if not _initialized:
        init(QMachineType.CPU)
        _initialized = True

    qvm = CPUQVM()
    qvm.init()
    qubits = qvm.qAlloc_many(n)

    prog = QProg()
    for i in range(n):
        prog << H(qubits[i])

    qvm.directlyRun(prog)
    state = qvm.getQState()
    return state
