# EVAL_META: task_id=116, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from qiskit.synthesis import MatrixExponential


def synthesize_evolution_gate(pauli_string, time):
    if not isinstance(pauli_string, str) or len(pauli_string) == 0:
        raise ValueError("pauli_string must be a non-empty string over {'I','X','Y','Z'}.")
    if any(ch not in "IXYZ" for ch in pauli_string):
        raise ValueError("pauli_string must contain only characters 'I', 'X', 'Y', 'Z'.")

    pauli_mats = {
        "I": np.array([[1, 0], [0, 1]], dtype=complex),
        "X": np.array([[0, 1], [1, 0]], dtype=complex),
        "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
        "Z": np.array([[1, 0], [0, -1]], dtype=complex),
    }

    hamiltonian = np.array([[1]], dtype=complex)
    for ch in pauli_string:
        hamiltonian = np.kron(hamiltonian, pauli_mats[ch])

    unitary = Operator(np.cos(time) * np.eye(hamiltonian.shape[0], dtype=complex) - 1j * np.sin(time) * hamiltonian)
    synth = MatrixExponential()
    return synth.run(unitary)
