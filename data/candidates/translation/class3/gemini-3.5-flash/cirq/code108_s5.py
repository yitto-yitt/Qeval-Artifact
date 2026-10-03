# EVAL_META: task_id=108, framework=cirq, class=3
import cirq
import numpy as np


def initialize_adjoint_and_compose(data1, data2):
    def to_matrix(data):
        if hasattr(data, "choi_matrix"):
            return data.choi_matrix
        return np.asarray(data)

    def choi_to_superop(J):
        d = int(np.sqrt(J.shape[0]))
        J_tensor = J.reshape((d, d, d, d))
        S_tensor = np.transpose(J_tensor, (3, 1, 2, 0))
        return S_tensor.reshape((d * d, d * d))

    def superop_to_choi(S):
        d = int(np.sqrt(S.shape[0]))
        S_tensor = S.reshape((d, d, d, d))
        J_tensor = np.transpose(S_tensor, (3, 1, 2, 0))
        return J_tensor.reshape((d * d, d * d))

    m1 = to_matrix(data1)
    m2 = to_matrix(data2)

    choi1 = cirq.Choi(m1)
    choi2 = cirq.Choi(m2)

    S1 = choi_to_superop(m1)
    S1_adj = S1.conj().T
    m1_adj = superop_to_choi(S1_adj)
    adjoint_choi1 = cirq.Choi(m1_adj)

    S2 = choi_to_superop(m2)
    S_composed = S1 @ S2
    m_composed = superop_to_choi(S_composed)
    composed_choi = cirq.Choi(m_composed)

    return choi1, adjoint_choi1, composed_choi
