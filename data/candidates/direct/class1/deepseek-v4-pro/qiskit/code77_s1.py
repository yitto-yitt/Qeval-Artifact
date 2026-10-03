# EVAL_META: task_id=77, framework=qiskit, class=1
from qiskit import QuantumCircuit
import numpy as np

def circuit_from_probability_dist(probability_dist):
    if not probability_dist:
        return QuantumCircuit()
    keys = list(probability_dist.keys())
    if isinstance(keys[0], str):
        num_qubits = len(keys[0])
    else:
        max_key = max(keys)
        num_qubits = max_key.bit_length() if max_key > 0 else 1

    statevector = np.zeros(2 ** num_qubits, dtype=complex)
    for key, prob in probability_dist.items():
        if isinstance(key, str):
            idx = int(key, 2)
        else:
            idx = key
        statevector[idx] = np.sqrt(prob)
    norm = np.linalg.norm(statevector)
    if norm > 0:
        statevector = statevector / norm
    qc = QuantumCircuit(num_qubits)
    qc.initialize(statevector.tolist(), range(num_qubits))
    return qc
