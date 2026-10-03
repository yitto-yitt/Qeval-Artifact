# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import QProg, X, CRY, CPUQVM

def tensor_circuits():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    prog = QProg()
    prog << CRY(qubits[0], qubits[1], 0.2)
    prog << X(qubits[2])
    return prog
