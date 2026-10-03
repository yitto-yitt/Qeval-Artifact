# EVAL_META: task_id=77, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation


def circuit_from_probability_dist(probability_dist):
    sample_key = next(iter(probability_dist))
    num_qubits = len(sample_key)

    statevector = np.zeros(2 ** num_qubits, dtype=complex)
    for bitstring, prob in probability_dist.items():
        index = int(bitstring, 2)
        statevector[index] = np.sqrt(prob)

    norm = np.linalg.norm(statevector)
    if norm > 0:
        statevector = statevector / norm

    qc = QuantumCircuit(num_qubits)
    qc.append(StatePreparation(statevector), range(num_qubits))

    return qc
