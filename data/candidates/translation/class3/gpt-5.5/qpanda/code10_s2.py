# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import *


def create_operator():
    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    prog = QProg()
    prog << X(qubits[0]) << X(qubits[1])
    create_operator._resources = (qvm, qubits)
    return prog
