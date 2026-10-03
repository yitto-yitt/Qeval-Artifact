# EVAL_META: task_id=40, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler


def init_random_3qubit(desired_vector):
    # Normalize the desired vector
    normalized_vector = desired_vector / np.linalg.norm(desired_vector)
    
    # Create a quantum circuit with 3 qubits
    qc = QuantumCircuit(3)
    
    # Initialize the circuit with the desired state
    qc.initialize(normalized_vector, [0, 1, 2])
    
    # Convert to Statevector to ensure proper initialization
    statevector = Statevector(qc)
    
    # Create a new circuit and initialize with the statevector
    qc_init = QuantumCircuit(3)
    qc_init.initialize(statevector, [0, 1, 2])
    
    # Add measurement gates
    qc_init.measure_all()
    
    # Use Aer simulator backend
    backend = AerSimulator()
    
    # Create sampler with the Aer simulator
    sampler = Sampler(backend)
    
    # Run the circuit and get results
    job = sampler.run([qc_init], shots=10000)
    result = job.result()
    
    # Extract probability distribution
    prob_dist = result.quasi_dists[0]
    
    # Convert to regular dict with bitstring keys
    final_dict = {}
    for key, value in prob_dist.items():
        bitstring = format(key, '03b')
        final_dict[bitstring] = value
    
    return final_dict
