# EVAL_META: task_id=77, framework=qiskit, class=1

import numpy as np
from qiskit import QuantumCircuit

def circuit_from_probability_dist(probability_dist):
    if not probability_dist:
        return QuantumCircuit()
    
    keys = list(probability_dist.keys())
    n_qubits = len(keys[0])
    
    state_vector = np.zeros(2**n_qubits)
    for bitstring, prob in probability_dist.items():
        idx = int(bitstring, 2)
        state_vector[idx] = np.sqrt(max(0.0, prob))
        
    norm = np.linalg.norm(state_vector)
    if norm > 0:
        state_vector = state_vector / norm
        
    qc = QuantumCircuit(n_qubits)
    qc.initialize(state_vector, range(n_qubits))
    qc.measure_all()
    return qc
