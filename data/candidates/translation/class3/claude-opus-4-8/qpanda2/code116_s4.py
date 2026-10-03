# EVAL_META: task_id=116, framework=qpanda2, class=3
import numpy as np
from scipy.linalg import expm
from pyqpanda import CPUQVM, QCircuit, matrix_decompose

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(12)


def synthesize_evolution_gate(pauli_string, time):
    I = np.array([[1, 0], [0, 1]], dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    pmap = {'I': I, 'X': X, 'Y': Y, 'Z': Z}

    mat = np.array([[1]], dtype=complex)
    for ch in pauli_string:
        mat = np.kron(mat, pmap[ch])

    n = len(pauli_string)
    U = expm(-1j * time * mat)

    used = qubits[:n]
    circ = matrix_decompose(used, U)
    return circ
