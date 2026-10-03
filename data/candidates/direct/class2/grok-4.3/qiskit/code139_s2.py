# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import DensityMatrix, Statevector

def schmidt_test(data, qargs_B):
    if isinstance(data, DensityMatrix):
        try:
            sv = data.to_statevector()
        except Exception:
            sv = Statevector(data)
    else:
        sv = Statevector(data)
    n = sv.num_qubits
    qargs_B = sorted(qargs_B)
    qargs_A = sorted([i for i in range(n) if i not in qargs_B])
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    vec = sv.data.reshape((2,) * n)
    desired_qubit_order = sorted(qargs_A, reverse=True) + sorted(qargs_B, reverse=True)
    axes = [n - 1 - q for q in desired_qubit_order]
    vec = np.transpose(vec, axes)
    mat = vec.reshape((dim_A, dim_B))
    U, S, Vh = np.linalg.svd(mat, full_matrices=False)
    terms = []
    for i, s in enumerate(S):
        if abs(s) < 1e-10:
            continue
        sv_A = Statevector(U[:, i])
        sv_B = Statevector(Vh[i, :])
        terms.append((s, sv_A, sv_B))
    return terms
