# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, X


def create_operator():
    machine = CPUQVM()
    qubits = machine.qAlloc_many(2)
    prog = QProg()
    prog << X(qubits[0]) << X(qubits[1])
    return prog
