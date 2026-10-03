# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import *

def inv_circuit(n):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n)

    prog = QProg()
    for i in range(2):
        prog << H(q[i + 1])
    for i in range(2):
        prog << CNOT(q[i + 1], q[i + 3])

    inv_prog = QProg()
    for i in range(1, -1, -1):
        inv_prog << CNOT(q[i + 1], q[i + 3])
    for i in range(1, -1, -1):
        inv_prog << H(q[i + 1])

    machine.finalize()
    return inv_prog
