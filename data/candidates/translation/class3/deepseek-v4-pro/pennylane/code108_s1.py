# EVAL_META: task_id=108, framework=pennylane, class=3
import numpy as np


def initialize_adjoint_and_compose(data1, data2):
    choi1 = np.asarray(data1)
    choi2 = np.asarray(data2)

    # adjoint is complex conjugate
    adjoint_choi1 = np.conj(choi1)

    # compose using superoperator representation
    n = choi1.shape[0]          # d^2
    d = int(np.sqrt(n))         # Hilbert space dimension

    # reshape Choi to tensor (i,j,k,l)
    J1 = choi1.reshape(d, d, d, d)
    J2 = choi2.reshape(d, d, d, d)

    # convert Choi -> superoperator: S[i,j,k,l] = J[i,k,j,l]
    S1 = J1.transpose(0, 2, 1, 3).reshape(n, n)
    S2 = J2.transpose(0, 2, 1, 3).reshape(n, n)

    # composition in superoperator representation
    S_comp = S1 @ S2

    # convert back: J[i,j,k,l] = S[i,k,j,l]
    J_comp = S_comp.reshape(d, d, d, d).transpose(0, 2, 1, 3).reshape(n, n)

    return choi1, adjoint_choi1, J_comp
