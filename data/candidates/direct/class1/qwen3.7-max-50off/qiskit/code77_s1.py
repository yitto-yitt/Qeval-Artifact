# EVAL_META: task_id=77, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation
import numpy as np

def circuit_from_probability_dist(probability_dist):
    sample_key = next(iter(probability_dist))
    num_qubits = len(sample_key)

    state_vector = np.zeros(2**num_qubits, dtype=complex)
    for bitstring, prob in probability_dist.items():
        index = int(bitstring, 2)
        state_vector[index] = np.sqrt(prob)

    norm = np.linalg.norm(state_vector)
    if norm > 0:
        state_vector = state_vector / norm

    qc = QuantumCircuit(num_qubits)
    state_prep = StatePreparation(state_vector)
    qc.append(state_prep, range(num_qubits))

    return qc
