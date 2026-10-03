# EVAL_META: task_id=116, framework=qpanda, class=3
import numpy as np
from scipy.linalg import expm
from pyqpanda3.core import QCircuit, QOracle


def synthesize_evolution_gate(pauli_string, time):
    paulis = {
        "I": np.eye(2, dtype=complex),
        "X": np.array([[0, 1], [1, 0]], dtype=complex),
        "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
        "Z": np.array([[1, 0], [0, -1]], dtype=complex),
    }

    if not isinstance(pauli_string, str) or not pauli_string:
        raise ValueError("pauli_string must be a nonempty string of I, X, Y, and Z.")
    if any(symbol not in paulis for symbol in pauli_string):
        raise ValueError("pauli_string may contain only I, X, Y, and Z.")

    hamiltonian = np.ones((1, 1), dtype=complex)
    for symbol in pauli_string:
        hamiltonian = np.kron(hamiltonian, paulis[symbol])

    unitary = expm(-1j * float(time) * hamiltonian)
    qubits = list(range(len(pauli_string)))

    try:
        gate = QOracle(qubits, unitary)
    except TypeError:
        try:
            gate = QOracle(qubits, unitary.tolist())
        except TypeError:
            gate = QOracle(qubits, unitary.ravel().tolist())

    circuit = QCircuit()
    circuit << gate
    return circuit
