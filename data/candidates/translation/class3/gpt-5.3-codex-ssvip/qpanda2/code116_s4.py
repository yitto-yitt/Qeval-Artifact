# EVAL_META: task_id=116, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(64)

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qubits = _global_qubits[:n]

    I = np.array([[1, 0], [0, 1]], dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)

    pauli_map = {'I': I, 'X': X, 'Y': Y, 'Z': Z}

    P = np.array([[1]], dtype=complex)
    for ch in pauli_string:
        P = np.kron(P, pauli_map[ch])

    dim = 2 ** n
    U = np.cos(time) * np.eye(dim, dtype=complex) - 1j * np.sin(time) * P

    prog = pq.QProg()
    prog << pq.matrix_decompose(qubits, U.flatten().tolist())

    return prog

machine.finalize()
