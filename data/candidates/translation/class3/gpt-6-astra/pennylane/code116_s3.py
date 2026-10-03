# EVAL_META: task_id=116, framework=pennylane, class=3
import numpy as np
import pennylane as qml
from scipy.linalg import expm


def synthesize_evolution_gate(pauli_string, time):
    matrices = {
        "I": np.eye(2, dtype=complex),
        "X": np.array([[0, 1], [1, 0]], dtype=complex),
        "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
        "Z": np.array([[1, 0], [0, -1]], dtype=complex),
    }
    hamiltonian = np.ones((1, 1), dtype=complex)
    for symbol in reversed(pauli_string):
        hamiltonian = np.kron(hamiltonian, matrices[symbol])

    unitary = expm(-1j * time * hamiltonian)
    wires = list(range(len(pauli_string)))
    return qml.tape.QuantumScript(
        [qml.QubitUnitary(unitary, wires=wires)]
    )
