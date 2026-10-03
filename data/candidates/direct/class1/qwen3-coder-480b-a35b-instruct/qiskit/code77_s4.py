# EVAL_META: task_id=77, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import numpy as np
from qiskit.extensions import Initialize


def circuit_from_probability_dist(probability_dist):
    # Determine the number of qubits needed based on the maximum measurement outcome
    max_key = max(probability_dist.keys(), key=lambda x: int(x, 2))
    num_qubits = len(max_key)
    
    # Create quantum and classical registers
    qc = QuantumCircuit(num_qubits)
    
    # Prepare the state vector from the probability distribution
    # First, we need to ensure all possible states up to the required number of qubits are included
    state_vector = [0] * (2 ** num_qubits)
    
    for measurement, prob in probability_dist.items():
        index = int(measurement, 2)
        state_vector[index] = np.sqrt(prob)  # Amplitude is square root of probability
    
    # Normalize the state vector if needed
    norm = np.linalg.norm(state_vector)
    if norm != 0:
        state_vector = state_vector / norm
    
    # Apply initialization to create the desired state
    init_gate = Initialize(state_vector)
    qc.append(init_gate, range(num_qubits))
    
    return qc
