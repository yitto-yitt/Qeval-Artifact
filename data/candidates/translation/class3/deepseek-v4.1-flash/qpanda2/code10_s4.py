# EVAL_META: task_id=10, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
cbits = machine.cAlloc_many(2)

def create_operator():
    prog = QProg()
    prog << X(qubits[0]) << X(qubits[1])
    return prog

machine.finalize()
