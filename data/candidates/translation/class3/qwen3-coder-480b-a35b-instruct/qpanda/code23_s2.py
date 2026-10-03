# EVAL_META: task_id=23, framework=qpanda, class=3
from pyqpanda3.core import *

def dj_constant_oracle():
    qvm = init_quantum_machine(QMachineType.CPU)
    q = qvm.qAlloc_many(3)
    prog = QProg()
    prog << X(q[2])
    finalize_quantum_machine(qvm)
    return prog
