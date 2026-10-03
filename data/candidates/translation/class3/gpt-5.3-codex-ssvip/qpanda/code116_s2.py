# EVAL_META: task_id=116, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import *

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    dim = 1 << n

    I2 = np.array([[1, 0], [0, 1]], dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)

    pauli_map = {"I": I2, "X": X, "Y": Y, "Z": Z}

    P = np.array([[1]], dtype=complex)
    for ch in pauli_string:
        if ch not in pauli_map:
            raise ValueError("pauli_string must contain only 'I', 'X', 'Y', 'Z'")
        P = np.kron(P, pauli_map[ch])

    vals, vecs = np.linalg.eigh(P)
    U = vecs @ np.diag(np.exp(-1j * time * vals)) @ vecs.conj().T

    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(n)

    prog = QProg()
    prog.insert(QOracle(q, U.reshape(-1).tolist()))
    qvm.finalize_qvm()
    return prog
