# EVAL_META: task_id=108, framework=cirq, class=3
import numpy as np


def initialize_adjoint_and_compose(data1, data2):
    choi1 = np.asarray(data1, dtype=complex)
    choi2 = np.asarray(data2, dtype=complex)
    adjoint_choi1 = choi1.conj().T
    composed_choi = choi1 @ choi2
    return choi1, adjoint_choi1, composed_choi
