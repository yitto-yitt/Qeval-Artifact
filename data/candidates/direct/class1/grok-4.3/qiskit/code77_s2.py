# EVAL_META: task_id=77, framework=qiskit, class=1
from qiskit import QuantumCircuit
import numpy as np

def circuit_from_probability_dist(probability_dist):
    bitstrings = list(probability_dist.keys())
    n_qubits = len(bitstrings[0])
    num_states = 2 ** n_qubits
    amplitudes = [0.0] * num_states
    for bitstring, prob in probability_dist.items():
        index = int(bitstring, 2)
        amplitudes[index] = np.sqrt(prob)
    qc = QuantumCircuit(n_qubits)
    qc.initialize(amplitudes, range(n_qubits))
    qc.measure_all()
    return qc
