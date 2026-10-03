# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import DensityMatrix, Statevector

def schmidt_test(data, qargs_B):
    try:
        dm = DensityMatrix(data)
        sv = dm.to_statevector()
    except Exception:
        sv = Statevector(data)
    n = sv.num_qubits
    psi = np.asarray(sv.data).flatten()
    qargs_B = list(qargs_B)
    qargs_A = [q for q in range(n) if q not in qargs_B]
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    psi_tensor = psi.reshape([2] * n)
    qargs_A_sorted = sorted(qargs_A, reverse=True)
    qargs_B_sorted = sorted(qargs_B, reverse=True)
    axes = [n - 1 - q for q in qargs_A_sorted] + [n - 1 - q for q in qargs_B_sorted]
    psi_tensor = psi_tensor.transpose(axes)
    psi_matrix = psi_tensor.reshape((dim_A, dim_B))
    U, S, Vh = np.linalg.svd(psi_matrix, full_matrices=False)
    terms = []
    for i in range(len(S)):
        if abs(S[i]) > 1e-12:
            coeff = float(S[i])
            vec_A = U[:, i]
            vec_B = Vh[i, :]
            terms.append((coeff, Statevector(vec_A), Statevector(vec_B)))
    return terms
