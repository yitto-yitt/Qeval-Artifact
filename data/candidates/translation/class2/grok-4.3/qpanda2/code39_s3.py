# EVAL_META: task_id=39, framework=qpanda2, class=2
from pyqpanda import *
def create_uniform_superposition(n):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    prog = QProg()
    for q in qubits:
        prog << H(q)
    qvm.directly_run(prog)
    result = qvm.get_qstate()
    qvm.finalize()
    return result
