# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np
import pennylane as qml
from pennylane import numpy as pnp


def schmidt_test(data, qargs_B):
    sv = np.asarray(getattr(data, "data", data)).ravel()
    n = int(round(np.log2(sv.size)))
    if (1 << n) != sv.size:
        raise ValueError("Statevector length must be a power of 2.")

    qargs_B = list(qargs_B)
    qargs_A = [q for q in range(n) if q not in qargs_B]

    nA = len(qargs_A)
    nB = len(qargs_B)

    tensor = sv.reshape([2] * n)
    perm = qargs_A + qargs_B
    tensor = np.transpose(tensor, perm)
    mat = tensor.reshape((1 << nA, 1 << nB))

    U, S, Vh = np.linalg.svd(mat, full_matrices=False)

    terms = []
    for i in range(len(S)):
        coeff = S[i]
        if coeff <= 1e-12:
            continue
        vecA = U[:, i]
        vecB = Vh[i, :].conj()
        terms.append((coeff, vecA, vecB))

    return terms
