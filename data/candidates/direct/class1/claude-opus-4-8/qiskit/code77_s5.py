# EVAL_META: task_id=77, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit


def circuit_from_probability_dist(probability_dist):
    keys = list(probability_dist.keys())
    num_qubits = len(next(iter(keys)))
    dim = 2 ** num_qubits
    amplitudes = np.zeros(dim, dtype=complex)
    for measurement, probability in probability_dist.items():
        index = int(measurement, 2)
        amplitudes[index] = np.sqrt(max(probability, 0.0))
    norm = np.linalg.norm(amplitudes)
    if norm == 0:
        amplitudes[0] = 1.0
    else:
        amplitudes = amplitudes / norm
    circuit = QuantumCircuit(num_qubits)
    circuit.initialize(amplitudes, range(num_qubits))
    circuit.measure_all()
    return circuit
