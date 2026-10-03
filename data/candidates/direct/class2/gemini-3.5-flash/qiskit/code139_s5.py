# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import Statevector, DensityMatrix

def schmidt_test(data, qargs_B):
    if isinstance(data, Statevector):
        psi = data.data
    elif isinstance(data, DensityMatrix):
        eigvals, eigvecs = np.linalg.eigh(data.data)
        psi = eigvecs[:, -1]
    elif isinstance(data, np.ndarray):
        if data.ndim == 1:
            psi = data
        elif data.ndim == 2:
            eigvals, eigvecs = np.linalg.eigh(data)
            psi = eigvecs[:, -1]
        else:
            raise ValueError("Invalid array dimension")
    else:
        try:
            psi = Statevector(data).data
        except Exception:
            dm = DensityMatrix(data)
            eigvals, eigvecs = np.linalg.eigh(dm.data)
            psi = eigvecs[:, -1]

    n = int(np.log2(len(psi)))
    qargs_B = sorted(list(qargs_B))
    qargs_A = sorted([i for i in range(n) if i not in qargs_B])

    axes_A = [n - 1 - q for q in reversed(qargs_A)]
    axes_B = [n - 1 - q for q in reversed(qargs_B)]

    psi_tensor = psi.reshape([2] * n)
    psi_transposed = np.transpose(psi_tensor, axes_A + axes_B)
    M = psi_transposed.reshape(2**len(qargs_A), 2**len(qargs_B))

    U, S, Vh = np.linalg.svd(M, full_matrices=False)

    results = []
    for i in range(len(S)):
        coeff = float(S[i])
        state_A = U[:, i]
        state_B = Vh[i, :]
        results.append((coeff, state_A, state_B))
    return results
