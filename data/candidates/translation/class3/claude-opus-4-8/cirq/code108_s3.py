# EVAL_META: task_id=108, framework=cirq, class=3
import numpy as np
import cirq


def _to_choi(data):
    if isinstance(data, np.ndarray):
        arr = np.asarray(data, dtype=complex)
        if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
            n = arr.shape[0]
            d = int(round(np.sqrt(n)))
            if d * d == n:
                return arr
        raise ValueError("Cannot interpret array as Choi matrix")

    if hasattr(data, "shape") and not isinstance(data, cirq.Gate):
        arr = np.asarray(data, dtype=complex)
        return _to_choi(arr)

    if isinstance(data, cirq.Gate):
        u = cirq.unitary(data)
    elif isinstance(data, cirq.Operation):
        u = cirq.unitary(data.gate)
    else:
        u = cirq.unitary(data)

    d = u.shape[0]
    choi = np.zeros((d * d, d * d), dtype=complex)
    for i in range(d):
        for j in range(d):
            e_ij = np.zeros((d, d), dtype=complex)
            e_ij[i, j] = 1.0
            mapped = u @ e_ij @ u.conj().T
            choi += np.kron(e_ij, mapped)
    return choi


def _choi_adjoint(choi):
    d2 = choi.shape[0]
    d = int(round(np.sqrt(d2)))
    # adjoint channel Choi: swap input/output and conjugate-transpose
    reshaped = choi.reshape(d, d, d, d)
    adj = np.conjugate(reshaped).transpose(2, 3, 0, 1)
    return adj.reshape(d2, d2)


def _choi_compose(choi1, choi2):
    # composed = choi2 after choi1 (choi1.compose(choi2) applies choi1 then choi2)
    d2 = choi1.shape[0]
    d = int(round(np.sqrt(d2)))

    def choi_to_superop(choi):
        r = choi.reshape(d, d, d, d)
        # choi index (i_out, i_in, j_out, j_in) -> superop
        sop = r.transpose(0, 2, 1, 3).reshape(d * d, d * d)
        return sop

    def superop_to_choi(sop):
        r = sop.reshape(d, d, d, d)
        c = r.transpose(0, 2, 1, 3).reshape(d * d, d * d)
        return c

    s1 = choi_to_superop(choi1)
    s2 = choi_to_superop(choi2)
    s_comp = s2 @ s1
    return superop_to_choi(s_comp)


def initialize_adjoint_and_compose(data1, data2):
    choi1 = _to_choi(data1)
    choi2 = _to_choi(data2)
    adjoint_choi1 = _choi_adjoint(choi1)
    composed_choi = _choi_compose(choi1, choi2)
    return choi1, adjoint_choi1, composed_choi
