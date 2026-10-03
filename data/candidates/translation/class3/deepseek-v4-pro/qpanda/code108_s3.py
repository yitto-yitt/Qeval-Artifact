# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np

try:
    from pyqpanda3.core import Choi as _PyQPandaChoi
except ImportError:
    _PyQPandaChoi = None


def initialize_adjoint_and_compose(data1, data2):
    if _PyQPandaChoi is not None:
        choi1 = _PyQPandaChoi(data1)
        choi2 = _PyQPandaChoi(data2)
        adjoint_choi1 = choi1.adjoint()
        composed_choi = choi1.compose(choi2)
        return choi1, adjoint_choi1, composed_choi

    choi1 = np.asarray(data1, dtype=complex)
    choi2 = np.asarray(data2, dtype=complex)

    n1 = choi1.shape[0]
    n2 = choi2.shape[0]
    d1 = int(np.sqrt(n1))
    d2 = int(np.sqrt(n2))

    if d1 * d1 != n1 or d2 * d2 != n2:
        raise ValueError("Choi matrix must be square with dimension d^2")
    if d1 != d2:
        raise ValueError("Choi matrices must have the same dimension")

    d = d1

    def choi_to_kraus(choi):
        w, v = np.linalg.eigh(choi)
        kraus = []
        tol = max(1e-14, np.max(np.abs(w)) * 1e-12)
        for lam, vec in zip(w, v.T):
            lam = float(np.real(lam))
            if lam <= tol:
                continue
            A = np.sqrt(lam) * vec.reshape((d, d), order='F')
            kraus.append(A)
        if not kraus:
            kraus.append(np.zeros((d, d), dtype=complex))
        return kraus

    def kraus_to_choi(kraus):
        choi = np.zeros((d * d, d * d), dtype=complex)
        for A in kraus:
            vec = A.flatten(order='F')
            choi += np.outer(vec, vec.conj())
        return choi

    kraus1 = choi_to_kraus(choi1)
    kraus2 = choi_to_kraus(choi2)

    adjoint_choi1 = kraus_to_choi([A.conj().T for A in kraus1])
    composed_choi = kraus_to_choi([A @ B for A in kraus1 for B in kraus2])

    return choi1.copy(), adjoint_choi1, composed_choi
