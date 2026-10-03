# EVAL_META: task_id=23, framework=qpanda, class=3
from pyqpanda3.core import *

def dj_constant_oracle():
    # Allocate 3 qubits from a local quantum virtual machine
    qvm = CPUQVM()
    qvm.initQVM()
    q = qvm.qAlloc_many(3)
    # Build the constant-one oracle: apply X to the output qubit (index 2)
    prog = QProg()
    prog << X(q[2])
    return prog
