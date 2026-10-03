# EVAL_META: task_id=108, framework=qpanda2, class=3
import pyqpanda as pq
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)
def initialize_adjoint_and_compose(data1, data2):
    prog1 = QProg()
    prog1 << H(q[0])
    prog2 = QProg()
    prog2 << X(q[1])
    adjoint_prog1 = prog1.dagger()
    composed_prog = prog1
    composed_prog << prog2
    return prog1, adjoint_prog1, composed_prog
machine.finalize()
