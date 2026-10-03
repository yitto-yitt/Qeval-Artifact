# EVAL_META: task_id=117, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def decompose_unitary(unitary):
    circuit = matrix_decompose(q, unitary)
    return circuit

machine.finalize()
