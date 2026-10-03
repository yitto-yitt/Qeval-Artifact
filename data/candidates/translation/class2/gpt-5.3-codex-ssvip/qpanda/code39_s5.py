# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg, H

def create_uniform_superposition(n):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    prog = QProg()
    for q in qubits:
        prog << H(q)
    state = qvm.get_qstate(prog)
    qvm.finalize()
    return state
