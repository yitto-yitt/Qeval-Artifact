# EVAL_META: task_id=77, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation


def circuit_from_probability_dist(probability_dist):
    sample_key = next(iter(probability_dist.keys()))
    n_qubits = len(sample_key)

    state_vector = np.zeros(2**n_qubits, dtype=complex)

    for bitstring, prob in probability_dist.items():
        index = int(bitstring, 2)
        state_vector[index] = np.sqrt(prob)

    norm = np.linalg.norm(state_vector)
    if norm > 0:
        state_vector = state_vector / norm

    qc = QuantumCircuit(n_qubits)
    qc.append(StatePreparation(state_vector), range(n_qubits))

    return qc
