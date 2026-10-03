# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import *

def initialize_adjoint_and_compose(data1, data2):
    choi1 = np.array(data1, dtype=complex)
    choi2 = np.array(data2, dtype=complex)
    adjoint_choi1 = choi1.conj().T
    composed_choi = choi1 @ choi2
    return choi1, adjoint_choi1, composed_choi
