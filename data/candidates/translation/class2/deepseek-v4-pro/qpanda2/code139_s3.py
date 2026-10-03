# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    def _schmidt_vector(statevec, qargs_B):
        statevec = np.asarray(statevec, dtype=complex)

        n = int(np.log2(statevec.size))
        if 2 ** n != statevec.size:
            raise ValueError("Statevector length must be a power of two")

        if isinstance(qargs_B, int):
            qargs_B = [qargs_B]
        qargs_B = list(qargs_B)

        if len(set(qargs_B)) != len(qargs_B):
            raise ValueError("Duplicate qargs_B entries")
        if any(q < 0 or q >= n for q in qargs_B):
            raise ValueError("qargs_B out of range")

        qargs_A = [i for i in range(n) if i not in qargs_B]

        if len(qargs_B) == 0:
            return [(1.0, statevec.copy(), np.array([1.0 + 0j], dtype=complex))]
        if len(qargs_A) == 0:
            return [(1.0, np.array([1.0 + 0j], dtype=complex), statevec.copy())]

        tensor = np.reshape(statevec, [2] * n)
        tensor = np.transpose(tensor, qargs_A + qargs_B)

        dim_a = 2 ** len(qargs_A)
        dim_b = 2 ** len(qargs_B)
        mat = np.reshape(tensor, (dim_a, dim_b))

        U, S, Vh = np.linalg.svd(mat)

        terms = []
        for i, s in enumerate(S):
            if s > 1e-15:
                terms.append((float(s), U[:, i].copy(), Vh[i].copy()))
        return terms

    arr = np.asarray(data, dtype=complex)

    if arr.ndim == 1:
        norm = np.linalg.norm(arr)
        if norm == 0:
            raise ValueError("Zero statevector")
        statevec = arr / norm
        return _schmidt_vector(statevec, qargs_B)

    if arr.ndim == 2:
        if arr.shape[0] != arr.shape[1]:
            raise ValueError("Density matrix must be square")

        trace = np.trace(arr)
        if np.isclose(trace, 0.0):
            raise ValueError("Density matrix has zero trace")

        rho = arr / trace
        eigvals, eigvecs = np.linalg.eigh(rho)

        idx = int(np.argmax(eigvals.real))
        if not np.isclose(eigvals[idx].real, 1.0, atol=1e-8):
            raise ValueError("Density matrix is not pure")

        statevec = eigvecs[:, idx]
        statevec = statevec / np.linalg.norm(statevec)
        return _schmidt_vector(statevec, qargs_B)

    raise ValueError("Input must be a statevector or density matrix")
