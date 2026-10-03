# EVAL_META: task_id=77, framework=qiskit, class=1

import numpy as np
from qiskit import QuantumCircuit

def circuit_from_probability_dist(probability_dist):
    """
    Given a distribution dictionary of the form {measurement: probability},
    return a quantum circuit that produces that distribution.
    """
    keys = list(probability_dist.keys())
    if not keys:
        raise ValueError("Empty probability distribution")
    
    # Determine number of qubits from the bitstring length
    first_key = keys[0]
    if isinstance(first_key, str):
        num_qubits = len(first_key)
    else:
        # Fallback if keys are integers
        max_val = max(keys)
        num_qubits = int(np.ceil(np.log2(max_val + 1))) if max_val > 0 else 1

    state_size = 2**num_qubits
    statevector = np.zeros(state_size, dtype=complex)
    
    for outcome, prob in probability_dist.items():
        if isinstance(outcome, str):
            idx = int(outcome, 2)
        else:
            idx = int(outcome)
        statevector[idx] = np.sqrt(prob)
        
    # Normalize the statevector to handle potential numerical precision issues
    norm = np.linalg.norm(statevector)
    if norm > 0:
        statevector /= norm
        
    qc = QuantumCircuit(num_qubits)
    qc.initialize(statevector, range(num_qubits))
    
    return qc
