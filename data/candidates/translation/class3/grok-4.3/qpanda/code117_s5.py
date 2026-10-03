# EVAL_META: task_id=117, framework=qpanda, class=3
from pyqpanda3.core import TwoQubitBasisDecomposer
from pyqpanda3.core import CXGate
import numpy as np

def decompose_unitary(unitary):
    decomposer = TwoQubitBasisDecomposer(CXGate())
    return decomposer(unitary)
