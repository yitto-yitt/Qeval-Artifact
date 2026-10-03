# EVAL_META: task_id=116, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(64)

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    if n <= 0:
        return pq.QProg()

    qubits = _global_qubits[:n]

    I = np.array([[1, 0], [0, 1]], dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)

    pauli_map = {'I': I, 'X': X, 'Y': Y, 'Z': Z}
    p = np.array([[1]], dtype=complex)
    for ch in pauli_string:
        if ch not in pauli_map:
            raise ValueError("pauli_string must contain only 'I', 'X', 'Y', 'Z'")
        p = np.kron(p, pauli_map[ch])

    vals, vecs = np.linalg.eigh(p)
    u = vecs @ np.diag(np.exp(-1j * time * vals)) @ vecs.conj().T

    gate = pq.matrix_decompose(qubits, u)
    prog = pq.QProg()
    prog.insert(gate)
    return prog

machine.finalize()
