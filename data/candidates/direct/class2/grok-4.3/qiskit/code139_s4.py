# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import DensityMatrix

def schmidt_test(data, qargs_B):
    dm = DensityMatrix(data)
    psi = dm.to_statevector()
    vec = psi.data
    n = psi.num_qubits
    q_B = sorted(set(qargs_B))
    q_A = sorted(set(range(n)) - set(q_B))
    num_A = len(q_A)
    num_B = len(q_B)
    dim_A = 2 ** num_A
    dim_B = 2 ** num_B
    tensor = vec.reshape([2] * n)
    def get_axis(q):
        return n - 1 - q
    A_qubits = sorted(q_A, reverse=True)
    B_qubits = sorted(q_B, reverse=True)
    axes = [get_axis(q) for q in A_qubits + B_qubits]
    tensor = tensor.transpose(axes)
    mat = tensor.reshape((dim_A, dim_B))
    U, S, Vh = np.linalg.svd(mat, full_matrices=False)
    terms = []
    for i in range(len(S)):
        if S[i] > 1e-10:
            coeff = float(S[i])
            vec_A = U[:, i]
            vec_B = Vh[i, :].conj()
            terms.append((coeff, vec_A, vec_B))
    return terms
