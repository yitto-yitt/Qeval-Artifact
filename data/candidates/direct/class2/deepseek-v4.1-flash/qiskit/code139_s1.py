# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np


def schmidt_test(data, qargs_B):
    rho = np.asarray(data, dtype=complex)
    N = rho.shape[0]
    n = int(round(np.log2(N)))

    qargs_B = list(qargs_B)
    qargs_A = [q for q in range(n) if q not in qargs_B]

    dA = 2 ** len(qargs_A)
    dB = 2 ** len(qargs_B)

    # Permute so tensor order is A, A', B, B' for operator-Schmidt decomposition
    perm = qargs_A + [q + n for q in qargs_A] + qargs_B + [q + n for q in qargs_B]
    rho_p = np.transpose(rho, perm)

    # Reshape into (dA^2, dB^2) matrix
    mat = rho_p.reshape(dA * dA, dB * dB)

    U, S, Vh = np.linalg.svd(mat, full_matrices=False)

    terms = []
    for k in range(len(S)):
        coeff = complex(S[k])
        a_vec = np.asarray(U[:, k]).astype(complex)
        b_vec = np.asarray(Vh[k, :]).astype(complex)
        terms.append((coeff, a_vec, b_vec))
    return terms
