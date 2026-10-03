# EVAL_META: task_id=108, framework=cirq, class=3
import numpy as np


def initialize_adjoint_and_compose(data1, data2):
    def _choi_to_kraus(choi):
        dim = int(np.sqrt(choi.shape[0]))
        vals, vecs = np.linalg.eigh(choi)
        kraus = []
        for val, vec in zip(vals, vecs.T):
            if val > 1e-8:
                kraus.append(np.sqrt(val) * vec.reshape((dim, dim), order='C'))
        return kraus

    def _kraus_to_choi(kraus, shape):
        if not kraus:
            return np.zeros(shape, dtype=complex)
        d_out, d_in = kraus[0].shape
        choi = np.zeros((d_out * d_in, d_out * d_in), dtype=complex)
        for k in kraus:
            choi += np.outer(k, k.conj())
        return choi

    choi1 = np.array(data1, dtype=complex)
    choi2 = np.array(data2, dtype=complex)

    kraus1 = _choi_to_kraus(choi1)
    kraus2 = _choi_to_kraus(choi2)

    adjoint_choi1 = _kraus_to_choi([k.conj().T for k in kraus1], choi1.shape)
    composed_choi = _kraus_to_choi([a @ b for a in kraus1 for b in kraus2], choi1.shape)

    return choi1, adjoint_choi1, composed_choi

