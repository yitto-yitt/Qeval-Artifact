# EVAL_META: task_id=77, framework=qiskit, class=1
from qiskit import QuantumCircuit
import math

def circuit_from_probability_dist(probability_dist):
    # Get the number of qubits needed
    num_qubits = len(list(probability_dist.keys())[0])
    
    # Create quantum circuit
    qc = QuantumCircuit(num_qubits)
    
    # Convert probability distribution to amplitudes
    probabilities = []
    states = []
    for state, prob in probability_dist.items():
        states.append(state)
        probabilities.append(math.sqrt(prob))
    
    # Normalize amplitudes
    norm = math.sqrt(sum(abs(a)**2 for a in probabilities))
    amplitudes = [a/norm for a in probabilities]
    
    # Initialize circuit with the desired state
    qc.initialize(amplitudes, range(num_qubits))
    
    return qc
