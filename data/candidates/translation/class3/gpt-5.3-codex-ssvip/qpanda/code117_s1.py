# EVAL_META: task_id=117, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def decompose_unitary(unitary):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    prog = QProg()
    u = np.array(unitary, dtype=complex)
    gate = QOracle(q, u.flatten().tolist())
    prog << gate
    machine.finalize_qvm()
    return prog
