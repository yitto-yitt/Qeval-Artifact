# EVAL_META: task_id=108, framework=cirq, class=3
import numpy as np
from cirq.qis import choi_to_kraus, kraus_to_choi


def initialize_adjoint_and_compose(data1, data2):
    choi1 = np.asarray(data1, dtype=complex)
    choi2 = np.asarray(data2, dtype=complex)
    adjoint_choi1 = choi1.conj().T
    kraus1 = choi_to_kraus(choi1)
    kraus2 = choi_to_kraus(choi2)
    composed_kraus = [np.asarray(k1) @ np.asarray(k2) for k1 in kraus1 for k2 in kraus2]
    composed_choi = kraus_to_choi(composed_kraus)
    return choi1, adjoint_choi1, composed_choi
