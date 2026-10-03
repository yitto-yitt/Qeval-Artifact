# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import DensityMatrix, Statevector


def schmidt_test(data, qargs_B):
    dm = DensityMatrix(data)
    num_qubits = dm.num_qubits
    if num_qubits is None:
        dim = dm.dim
        n = int(round(np.log2(dim)))
        if 2**n != dim:
            raise ValueError("Input dimension is not a power of 2.")
        num_qubits = n

    qargs_B = list(qargs_B)
    if any((q < 0 or q >= num_qubits) for q in qargs_B):
        raise ValueError("qargs_B contains invalid qubit indices.")
    if len(set(qargs_B)) != len(qargs_B):
        raise ValueError("qargs_B contains duplicate qubit indices.")

    qargs_A = [q for q in range(num_qubits) if q not in qargs_B]

    evals, evecs = np.linalg.eigh(dm.data)
    idx = int(np.argmax(evals.real))
    if evals[idx].real < 1 - 1e-8:
        raise ValueError("Density matrix is not pure; Schmidt decomposition requires a pure state.")

    psi = evecs[:, idx]
    purity = float(np.real(np.trace(dm.data @ dm.data)))
    if abs(purity - 1.0) > 1e-6:
        raise ValueError("Density matrix is not pure; Schmidt decomposition requires a pure state.")

    sv = Statevector(psi)
    terms = sv.schmidt_decomposition(qargs_B=qargs_B)

    out = []
    for coeff, vec_a, vec_b in terms:
        out.append((complex(coeff), np.asarray(vec_a.data, dtype=complex), np.asarray(vec_b.data, dtype=complex)))
    return out
