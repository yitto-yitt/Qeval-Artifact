# EVAL_META: task_id=108, framework=qpanda2, class=3
import pyqpanda as pq
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
def initialize_adjoint_and_compose(data1, data2):
    prog1 = QProg()
    prog1 << H(qubits[0])
    prog2 = QProg()
    prog2 << X(qubits[1])
    adjoint_choi1 = prog1.dagger()
    composed_choi = QProg()
    composed_choi << prog1 << prog2
    return prog1, adjoint_choi1, composed_choi
machine.finalize()
