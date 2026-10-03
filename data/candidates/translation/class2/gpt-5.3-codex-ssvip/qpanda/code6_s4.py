# EVAL_META: task_id=6, framework=qpanda, class=2
from pyqpanda3.core import *


def create_state_prep(num_qubits):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(num_qubits)
    prog = QProg()
    if num_qubits > 0:
        prog << X(q[0])
    return prog
