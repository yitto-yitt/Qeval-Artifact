# EVAL_META: task_id=5, framework=qpanda2, class=2
from pyqpanda import *


def create_state_prep():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    prog = QProg()
    prog << X(qubits[0])
    return prog
