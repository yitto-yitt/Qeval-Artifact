# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
from pyqpanda import QMachineType, init_quantum_machine, destroy_quantum_machine


def schmidt_test(data, qargs_B):
    qvm = init_quantum_machine(QMachineType.CPU)

    try:
        state = np.asarray(data, dtype=complex)

        if state.ndim == 2:
            evals, evecs = np.linalg.eigh(state)
            idx = int(np.argmax(evals.real))
            state = evecs[:, idx]

        state = np.asarray(state, dtype=complex).reshape(-1)

        total_dim = state.shape[0]
        n = int(round(np.log2(total_dim)))
        if 2 ** n != total_dim:
            raise ValueError("State dimension must be a power of 2")

        qargs_B = list(qargs_B)
        b_set = set(qargs_B)
        qargs_A = [q for q in range(n) if q not in b_set]

        nA = len(qargs_A)
        nB = len(qargs_B)
        dimA = 2 ** nA
        dimB = 2 ** nB

        def bit_of(index, qubit):
            return (index >> qubit) & 1

        M = np.zeros((dimA, dimB), dtype=complex)
        for idx in range(total_dim):
            a_index = 0
            for pos, q in enumerate(qargs_A):
                a_index |= bit_of(idx, q) << pos
            b_index = 0
            for pos, q in enumerate(qargs_B):
                b_index |= bit_of(idx, q) << pos
            M[a_index, b_index] = state[idx]

        U, s, Vh = np.linalg.svd(M, full_matrices=False)

        terms = []
        for k in range(len(s)):
            coeff = float(s[k])
            if coeff <= 1e-12:
                continue
            vec_A = U[:, k].reshape(dimA)
            vec_B = Vh[k, :].reshape(dimB)
            terms.append((coeff, vec_A, vec_B))

        return terms

    finally:
        destroy_quantum_machine(qvm)
