# EVAL_META: task_id=108, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def _reshuffle(mat, shape):
    return np.reshape(
        np.transpose(np.reshape(mat, shape), (3, 1, 2, 0)),
        (shape[3] * shape[1], shape[0] * shape[2]),
    )


def _choi_to_superop(data, input_dim, output_dim):
    shape = (input_dim, output_dim, input_dim, output_dim)
    return _reshuffle(data, shape)


def _superop_to_choi(data, input_dim, output_dim):
    shape = (output_dim, output_dim, input_dim, input_dim)
    return _reshuffle(data, shape)


def initialize_adjoint_and_compose(data1, data2):
    choi1 = np.array(data1, dtype=complex)
    choi2 = np.array(data2, dtype=complex)

    d1 = int(round(np.sqrt(choi1.shape[0])))
    d2 = int(round(np.sqrt(choi2.shape[0])))

    # Adjoint of choi1: adjoint superoperator is the Hermitian conjugate
    s1 = _choi_to_superop(choi1, d1, d1)
    s1_adj = s1.conj().T
    adjoint_choi1 = _superop_to_choi(s1_adj, d1, d1)

    # Compose: choi1 first, then choi2  ->  S = S2 @ S1
    s2 = _choi_to_superop(choi2, d2, d2)
    s_comp = s2 @ s1
    composed_choi = _superop_to_choi(s_comp, d1, d2)

    return choi1, adjoint_choi1, composed_choi
