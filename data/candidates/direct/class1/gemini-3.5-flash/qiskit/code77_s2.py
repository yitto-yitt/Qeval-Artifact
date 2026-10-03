# EVAL_META: task_id=77, framework=qiskit, class=1
import math
from qiskit import QuantumCircuit

def circuit_from_probability_dist(probability_dist):
    if not probability_dist:
        return QuantumCircuit()
    
    # Determine the number of qubits from the length of the bitstrings
    bitstrings = list(probability_dist.keys())
    n_qubits = len(bitstrings[0])
    
    # Create the target statevector
    statevector = [0.0] * (2 ** n_qubits)
    for bitstring, prob in probability_dist.items():
        idx = int(bitstring, 2)
        statevector[idx] = math.sqrt(prob)
        
    # Create the quantum circuit and initialize it to the target state
    qc = QuantumCircuit(n_qubits)
    qc.initialize(statevector, range(n_qubits))
    
    return qc
