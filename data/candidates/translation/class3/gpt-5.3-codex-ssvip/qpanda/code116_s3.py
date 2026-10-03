# EVAL_META: task_id=116, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, matrix_decompose


def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    I = np.array([[1, 0], [0, 1]], dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)

    pmap = {"I": I, "X": X, "Y": Y, "Z": Z}
    P = np.array([[1]], dtype=complex)
    for ch in pauli_string:
        P = np.kron(P, pmap[ch])

    evals, evecs = np.linalg.eigh(P)
    U = evecs @ np.diag(np.exp(-1j * time * evals)) @ np.conjugate(evecs).T

    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    prog = QProg()
    prog.insert(matrix_decompose(qubits, U))
    return prog
