# EVAL_META: task_id=11, framework=qpanda2, class=2
from pyqpanda import CPUQVM, QProg

def get_statevector(circuit):
    qvm = CPUQVM()
    qvm.init_qvm()
    prog = QProg()
    prog << circuit
    qubits = prog.get_qubits()
    if qubits:
        n = max(q.index for q in qubits) + 1
    else:
        n = 0
    qvm.qAlloc_many(n)
    qvm.run(prog)
    state = qvm.get_qstate()
    return state
