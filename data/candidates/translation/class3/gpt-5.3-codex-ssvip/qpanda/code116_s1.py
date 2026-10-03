# EVAL_META: task_id=116, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import *


def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    dim = 1 << n

    I = np.array([[1, 0], [0, 1]], dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)

    pmap = {'I': I, 'X': X, 'Y': Y, 'Z': Z}
    P = np.array([[1]], dtype=complex)
    for ch in pauli_string:
        if ch not in pmap:
            raise ValueError("pauli_string must contain only 'I', 'X', 'Y', 'Z'")
        P = np.kron(P, pmap[ch])

    eigvals, eigvecs = np.linalg.eigh(P)
    U = eigvecs @ np.diag(np.exp(-1j * time * eigvals)) @ eigvecs.conj().T

    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(n)

    prog = QProg()
    prog << matrix_decompose(q, U)
    qvm.finalize_qvm()
    return prog
