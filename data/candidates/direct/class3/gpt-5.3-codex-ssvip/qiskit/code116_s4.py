# EVAL_META: task_id=116, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import HamiltonianGate


def synthesize_evolution_gate(pauli_string, time):
    pauli_string = str(pauli_string).upper()
    if len(pauli_string) == 0:
        return QuantumCircuit(0)

    pauli_mats = {
        "I": np.array([[1, 0], [0, 1]], dtype=complex),
        "X": np.array([[0, 1], [1, 0]], dtype=complex),
        "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
        "Z": np.array([[1, 0], [0, -1]], dtype=complex),
    }

    try:
        hamiltonian = pauli_mats[pauli_string[0]]
        for p in pauli_string[1:]:
            hamiltonian = np.kron(hamiltonian, pauli_mats[p])
    except KeyError as exc:
        raise ValueError("pauli_string must contain only 'I', 'X', 'Y', and 'Z'.") from exc

    n = len(pauli_string)
    qc = QuantumCircuit(n)
    evo_gate = HamiltonianGate(hamiltonian, float(time))
    qc.append(evo_gate, list(range(n)))
    return qc
