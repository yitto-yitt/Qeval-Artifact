# EVAL_META: task_id=116, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(64)

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qubits = _global_qubits[:n]

    pauli_mats = {
        'I': np.array([[1, 0], [0, 1]], dtype=complex),
        'X': np.array([[0, 1], [1, 0]], dtype=complex),
        'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
        'Z': np.array([[1, 0], [0, -1]], dtype=complex),
    }

    P = np.array([[1]], dtype=complex)
    for ch in pauli_string:
        if ch not in pauli_mats:
            raise ValueError("pauli_string must contain only 'I', 'X', 'Y', 'Z'")
        P = np.kron(P, pauli_mats[ch])

    dim = 2 ** n
    I = np.eye(dim, dtype=complex)
    U = np.cos(time) * I - 1j * np.sin(time) * P

    prog = pq.QProg()
    gate = pq.matrix_decompose(qubits, U.tolist())
    prog.insert(gate)

    machine.finalize()
    return prog
