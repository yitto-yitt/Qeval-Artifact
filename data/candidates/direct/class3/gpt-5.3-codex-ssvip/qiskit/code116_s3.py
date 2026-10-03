# EVAL_META: task_id=116, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import HamiltonianGate

def synthesize_evolution_gate(pauli_string, time):
    if not isinstance(pauli_string, str) or len(pauli_string) == 0:
        raise ValueError("pauli_string must be a non-empty string.")
    if not all(ch in "IXYZ" for ch in pauli_string):
        raise ValueError("pauli_string must contain only characters in 'I', 'X', 'Y', 'Z'.")

    pauli_mats = {
        "I": np.array([[1, 0], [0, 1]], dtype=complex),
        "X": np.array([[0, 1], [1, 0]], dtype=complex),
        "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
        "Z": np.array([[1, 0], [0, -1]], dtype=complex),
    }

    hamiltonian = np.array([[1]], dtype=complex)
    for p in pauli_string:
        hamiltonian = np.kron(hamiltonian, pauli_mats[p])

    n_qubits = len(pauli_string)
    qc = QuantumCircuit(n_qubits)
    evo_gate = HamiltonianGate(hamiltonian, float(time))
    qc.append(evo_gate, range(n_qubits))
    return qc
