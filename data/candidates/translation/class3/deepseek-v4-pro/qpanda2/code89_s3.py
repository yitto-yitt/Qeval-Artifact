# EVAL_META: task_id=89, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init()
qubits = machine.qAlloc_many(3)

def create_controlled_hgate():
    prog = QProg()
    c3h = H(qubits[2]).control([qubits[0], qubits[1]])
    prog << c3h
    return prog

machine.finalize()
