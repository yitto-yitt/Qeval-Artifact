# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import *

def create_uniform_superposition(n):
    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    qubits = qvm.qAlloc_many(n) if n > 0 else []
    prog = QProg()

    for i in range(n):
        prog << H(qubits[i])

    if hasattr(qvm, "directly_run"):
        qvm.directly_run(prog)
    elif hasattr(qvm, "run"):
        qvm.run(prog)
    else:
        qvm.execute(prog)

    if hasattr(qvm, "get_qstate"):
        return qvm.get_qstate()
    if hasattr(qvm, "get_qstate_vector"):
        return qvm.get_qstate_vector()
    return qvm.get_statevector()
