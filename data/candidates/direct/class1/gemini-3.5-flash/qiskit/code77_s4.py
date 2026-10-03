# EVAL_META: task_id=77, framework=qiskit, class=1

import numpy as np
from qiskit import QuantumCircuit

def circuit_from_probability_dist(probability_dist):
    if not probability_dist:
        return QuantumCircuit()
    
    # Get the number of qubits from the length of the keys
    keys = list(probability_dist.keys())
    num_qubits = len(keys[0])
    
    # Initialize statevector with zeros
    state_size = 2**num_qubits
    statevector = np.zeros(state_size, dtype=complex)
    
    for bitstring, prob in probability_dist.items():
        idx = int(bitstring, 2)
        statevector[idx] = np.sqrt(prob)
        
    # Create quantum circuit and initialize it to the desired state
    qc = QuantumCircuit(num_qubits)
    qc.initialize(statevector, range(num_qubits))
    
    return qc
