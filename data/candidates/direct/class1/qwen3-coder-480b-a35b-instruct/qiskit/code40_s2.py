# EVAL_META: task_id=40, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.primitives import Sampler


def init_random_3qubit(desired_vector):
    # Normalize the desired vector
    normalized_vector = desired_vector / np.linalg.norm(desired_vector)

    # Create a quantum circuit with 3 qubits
    qc = QuantumCircuit(3)

    # Initialize the quantum circuit to the desired state
    qc.initialize(normalized_vector, [0, 1, 2])

    # Add measurements to all qubits
    qc.measure_all()

    # Use Aer simulator backend
    backend = AerSimulator()

    # Create a sampler instance
    sampler = Sampler(backend=backend)

    # Run the sampler
    result = sampler.run(qc).result()

    # Get the quasi-probabilities (probabilities) from the result
    quasi_dist = result.quasi_dists[0]

    # Convert the quasi-distribution to a regular probability distribution dictionary
    prob_dist = {}
    for outcome, prob in quasi_dist.items():
        # Convert integer outcome to binary string with 3 bits
        bitstring = format(outcome, '03b')
        prob_dist[bitstring] = prob

    return prob_dist
