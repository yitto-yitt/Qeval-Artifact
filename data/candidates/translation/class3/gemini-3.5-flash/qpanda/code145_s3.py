# EVAL_META: task_id=145, framework=qpanda, class=3
from pyqpanda3.core import *

def qft_inverse(n):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    return QFT(qubits).dagger()
