# EVAL_META: task_id=77, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation


def circuit_from_probability_dist(probability_dist):
    num_qubits = len(next(iter(probability_dist.keys())))
    state_vector = np.zeros(2**num_qubits, dtype=complex)
    for bitstring, prob in probability_dist.items():
        index = int(bitstring, 2)
        state_vector[index] = np.sqrt(prob)
    qc = QuantumCircuit(num_qubits)
    sp = StatePreparation(state_vector)
    qc.append(sp, range(num_qubits))
    return qc
