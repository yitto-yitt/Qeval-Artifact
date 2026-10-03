# EVAL_META: task_id=117, framework=qpanda2, class=3
from pyqpanda import *
from pyqpanda.Algorithm import two_qubit_decompose
import numpy as np

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def decompose_unitary(unitary):
    return two_qubit_decompose(unitary, q[0], q[1])

machine.finalize()
