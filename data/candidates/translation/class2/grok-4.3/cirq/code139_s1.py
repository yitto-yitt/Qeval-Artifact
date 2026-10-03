# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    psi = np.asarray(data, dtype=complex).ravel()
    n_qubits = int(np.log2(psi.size))
    qargs_A = sorted(set(range(n_qubits)) - set(qargs_B))
    tensor = psi.reshape([2] * n_qubits)
    def get_axis(q):
        return n_qubits - 1 - q
    qargs_A_sorted = sorted(qargs_A)
    qargs_B_sorted = sorted(qargs_B)
    axes_order = [get_axis(q) for q in qargs_A_sorted] + [get_axis(q) for q in qargs_B_sorted]
    tensor = tensor.transpose(axes_order)
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    mat = tensor.reshape(dim_A, dim_B)
    U, S, Vh = np.linalg.svd(mat, full_matrices=False)
    terms = []
    for i, s in enumerate(S):
        if s > 1e-10:
            vecA = U[:, i]
            vecB = Vh[i, :]
            terms.append((s, vecA, vecB))
    return terms
