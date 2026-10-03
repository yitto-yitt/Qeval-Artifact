# EVAL_META: task_id=77, framework=qiskit, class=1
import math
from qiskit import QuantumCircuit

def circuit_from_probability_dist(probability_dist):
    if not probability_dist:
        raise ValueError("Probability distribution cannot be empty.")
    
    # Determine the number of qubits from the length of the bitstrings
    bitstrings = list(probability_dist.keys())
    num_qubits = len(bitstrings[0])
    
    # Initialize statevector with zeros
    statevector = [0.0] * (2 ** num_qubits)
    
    # Normalize the probabilities to avoid precision issues
    total_prob = sum(probability_dist.values())
    if total_prob <= 0:
        raise ValueError("Total probability must be greater than zero.")
        
    for bitstring, prob in probability_dist.items():
        idx = int(bitstring, 2)
        statevector[idx] = math.sqrt(prob / total_prob)
        
    qc = QuantumCircuit(num_qubits)
    qc.initialize(statevector, range(num_qubits))
    qc.measure_all()
    
    return qc
