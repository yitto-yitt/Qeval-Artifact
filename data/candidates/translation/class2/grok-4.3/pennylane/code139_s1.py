# EVAL_META: task_id=139, framework=pennylane, class=2
import pennylane as qml
import numpy as np

def schmidt_test(data, qargs_B):
    if isinstance(data, qml.numpy.ndarray):
        data = np.array(data)
    if data.ndim == 2:
        evals, evecs = np.linalg.eigh(data)
        idx = np.argmax(evals)
        vec = evecs[:, idx]
        if np.iscomplexobj(data):
            vec = vec * np.exp(-1j * np.angle(vec[0]))
        data = vec
    n = int(np.log2(data.shape[0]))
    nb = len(qargs_B)
    na = n - nb
    dims = [2] * n
    psi = data.reshape(dims)
    all_qubits = list(range(n))
    a_qubits = [q for q in all_qubits if q not in qargs_B]
    move_to_front = a_qubits + qargs_B
    psi = np.transpose(psi, move_to_front)
    psi = psi.reshape(2**na, 2**nb)
    U, S, Vh = np.linalg.svd(psi, full_matrices=False)
    terms = []
    for i, s in enumerate(S):
        if abs(s) > 1e-12:
            va = U[:, i]
            vb = Vh[i, :]
            terms.append((s, va, vb))
    return terms
