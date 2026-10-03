# EVAL_META: task_id=116, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq
from scipy.linalg import expm

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(29)


def synthesize_evolution_gate(pauli_string, time):
    if not isinstance(pauli_string, str) or not pauli_string:
        raise ValueError("pauli_string must be a nonempty string.")
    if any(symbol not in "IXYZ" for symbol in pauli_string):
        raise ValueError("pauli_string must contain only I, X, Y, and Z.")
    if len(pauli_string) > len(qubits):
        raise ValueError("The Pauli string exceeds the allocated qubit capacity.")

    paulis = {
        "I": np.eye(2, dtype=complex),
        "X": np.array([[0, 1], [1, 0]], dtype=complex),
        "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
        "Z": np.array([[1, 0], [0, -1]], dtype=complex),
    }

    operator = np.ones((1, 1), dtype=complex)
    for symbol in pauli_string:
        operator = np.kron(operator, paulis[symbol])

    unitary = expm(-1j * float(time) * operator)
    return pq.matrix_decompose(qubits[:len(pauli_string)], unitary)


atexit.register(lambda: machine.finalize())
