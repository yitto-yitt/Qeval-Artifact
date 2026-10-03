# EVAL_META: task_id=39, framework=qpanda2, class=2
from pyqpanda import *

def create_uniform_superposition(n):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    prog = QProg()
    for i in range(n):
        prog << H(qubits[i])
    qvm.directly_run(prog)
    return qvm.get_qstate()
