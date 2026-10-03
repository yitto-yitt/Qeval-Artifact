# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import DensityMatrix, Statevector

def schmidt_test(data, qargs_B):
    rho = DensityMatrix(data)
    psi = rho.to_statevector()
    n_qubits = psi.num_qubits
    qargs_B = list(qargs_B)
    qargs_A = [q for q in range(n_qubits) if q not in qargs_B]
    qargs_A_sorted = sorted(qargs_A)
    qargs_B_sorted = sorted(qargs_B)
    shape = [2] * n_qubits
    tensor = psi.data.reshape(shape)
    def get_axis(q):
        return n_qubits - 1 - q
    axes_A = [get_axis(q) for q in qargs_A_sorted]
    axes_B = [get_axis(q) for q in qargs_B_sorted]
    new_axes = axes_A + axes_B
    tensor_permuted = tensor.transpose(new_axes)
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    mat = tensor_permuted.reshape((dim_A, dim_B))
    U, S, Vh = np.linalg.svd(mat, full_matrices=False)
    terms = []
    for i in range(len(S)):
        if abs(S[i]) > 1e-10:
            coeff = float(S[i])
            vec_A = U[:, i]
            vec_B = Vh[i, :].conj()
            sv_A = Statevector(vec_A)
            sv_B = Statevector(vec_B)
            terms.append((coeff, sv_A, sv_B))
    return terms
