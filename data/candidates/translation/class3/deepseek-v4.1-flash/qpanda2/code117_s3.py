# EVAL_META: task_id=117, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def decompose_unitary(unitary):
    return decompose(unitary, qubits)

machine.finalize()
