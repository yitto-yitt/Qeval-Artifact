# EVAL_META: task_id=6, framework=qpanda2, class=2
from pyqpanda import *


def create_state_prep(num_qubits):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(num_qubits)
    prog = QProg()
    prog << X(qubits[0])
    return prog
