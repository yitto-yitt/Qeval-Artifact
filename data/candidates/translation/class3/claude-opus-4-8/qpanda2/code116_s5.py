# EVAL_META: task_id=116, framework=qpanda2, class=3
import numpy as np
from scipy.linalg import expm
from pyqpanda import CPUQVM, QCircuit, matrix_decompose

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(12)


def _pauli_matrix(p):
    I = np.array([[1, 0], [0, 1]], dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    return {'I': I, 'X': X, 'Y': Y, 'Z': Z}[p]


def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    # Build full Pauli operator matrix (Qiskit ordering: leftmost char is highest qubit)
    mat = np.array([[1.0 + 0j]])
    for ch in pauli_string:
        mat = np.kron(mat, _pauli_matrix(ch))
    # exp(-i * time * P)
    U = expm(-1j * time * mat)

    qlist = [qubits[i] for i in range(n)]
    circuit = matrix_decompose(qlist, U)
    return circuit


if __name__ == "__main__":
    qc = synthesize_evolution_gate("XZ", 0.5)
    print(qc)
    machine.finalize()
