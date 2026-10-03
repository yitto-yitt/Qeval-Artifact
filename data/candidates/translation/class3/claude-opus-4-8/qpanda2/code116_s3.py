# EVAL_META: task_id=116, framework=qpanda2, class=3
import numpy as np
from scipy.linalg import expm
from pyqpanda import CPUQVM, QCircuit, matrix_decompose

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(12)

def synthesize_evolution_gate(pauli_string, time):
    ps = pauli_string
    n = len(ps)

    I = np.array([[1, 0], [0, 1]], dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    pmap = {'I': I, 'X': X, 'Y': Y, 'Z': Z}

    # Qiskit Pauli labels are read left-to-right as qubit n-1 ... qubit 0.
    # Build full operator with tensor ordering matching Qiskit (qubit 0 is rightmost).
    full = np.array([[1]], dtype=complex)
    for ch in ps:
        full = np.kron(full, pmap[ch])

    U = expm(-1j * time * full)

    used = qubits[:n]
    circ = QCircuit()
    circ << matrix_decompose(used, U)
    return circ
