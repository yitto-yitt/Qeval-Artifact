# EVAL_META: task_id=117, framework=qpanda, class=3
from pyqpanda3.core import two_qubit_decompose
import numpy as np

def decompose_unitary(unitary):
    return two_qubit_decompose(unitary)

