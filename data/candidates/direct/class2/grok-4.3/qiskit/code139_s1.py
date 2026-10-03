# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import DensityMatrix, Statevector

def schmidt_test(data, qargs_B):
    dm = DensityMatrix(data)
    sv = dm.to_statevector()
    psi = np.asarray(sv.data).flatten()
    n = sv.num_qubits
    qargs_A = [i for i in range(n) if i not in set(qargs_B)]
    qargs_A_desc = sorted(qargs_A, reverse=True)
    qargs_B_desc = sorted(qargs_B, reverse=True)
    axes = [n - 1 - q for q in qargs_A_desc + qargs_B_desc]
    tensor = psi.reshape([2] * n).transpose(axes).reshape(2 ** len(qargs_A), 2 ** len(qargs_B))
    U, S, Vh = np.linalg.svd(tensor, full_matrices=False)
    terms = []
    for i in range(len(S)):
        if abs(S[i]) < 1e-12:
            continue
        va = Statevector(U[:, i])
        vb = Statevector(Vh[i, :].conj())
        terms.append((float(S[i]), va, vb))
    return terms
