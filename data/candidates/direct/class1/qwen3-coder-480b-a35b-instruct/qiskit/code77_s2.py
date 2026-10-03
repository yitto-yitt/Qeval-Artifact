# EVAL_META: task_id=77, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import numpy as np
from qiskit.extensions import Initialize


def circuit_from_probability_dist(probability_dist):
    # Determine the number of qubits needed based on the keys in the distribution
    max_key_len = max(len(key) for key in probability_dist.keys())
    num_qubits = max_key_len
    
    # Create quantum and classical registers
    qc = QuantumCircuit(num_qubits)
    
    # Prepare the state vector from the probability distribution
    # First, we need to sort the keys to ensure consistent ordering
    sorted_keys = sorted(probability_dist.keys())
    
    # Create the amplitude vector (square root of probabilities with appropriate phases)
    n_states = 2 ** num_qubits
    amplitudes = [0] * n_states
    
    for key, prob in probability_dist.items():
        # Convert binary string key to integer index
        idx = int(key, 2)
        # Set the amplitude as the square root of the probability
        amplitudes[idx] = np.sqrt(prob)
    
    # Normalize the amplitudes
    norm_factor = np.linalg.norm(amplitudes)
    if norm_factor != 0:
        amplitudes = [amp / norm_factor for amp in amplitudes]
    
    # Initialize the quantum circuit with the desired state
    init_gate = Initialize(amplitudes)
    qc.append(init_gate, list(range(num_qubits)))
    
    return qc
