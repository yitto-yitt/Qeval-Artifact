# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg, H, qAlloc_many

def create_uniform_superposition(n):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    prog = QProg()
    for qubit in qubits:
        prog << H(qubit)
    qvm.directly_run(prog)
    state = qvm.get_qstate()
    qvm.finalize()
    return state
