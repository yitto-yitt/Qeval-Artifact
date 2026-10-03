# EVAL_META: task_id=117, framework=qpanda2, class=3
from pyqpanda import *
from pyqpanda import UnitaryDecomposer
import numpy as np

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def decompose_unitary(unitary):
    decomposer = UnitaryDecomposer()
    return decomposer.decompose(np.asarray(unitary, dtype=complex), q)

machine.finalize()
