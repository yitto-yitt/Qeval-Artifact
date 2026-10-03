# EVAL_META: task_id=77, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit


def circuit_from_probability_dist(probability_dist):
    keys = list(probability_dist.keys())
    num_qubits = len(next(iter(keys)))
    dim = 2 ** num_qubits
    amplitudes = np.zeros(dim, dtype=complex)
    for state, prob in probability_dist.items():
        index = int(state, 2)
        amplitudes[index] = np.sqrt(prob)
    norm = np.linalg.norm(amplitudes)
    if norm > 0:
        amplitudes = amplitudes / norm
    qc = QuantumCircuit(num_qubits)
    qc.initialize(amplitudes, range(num_qubits))
    qc.measure_all()
    return qc
