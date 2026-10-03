# EVAL_META: task_id=40, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer.primitives import Sampler

def init_random_3qubit(desired_vector):
    # Initialize a 3-qubit quantum circuit
    qc = QuantumCircuit(3)
    qc.initialize(desired_vector)
    qc.measure_all()
    
    # Use the Aer Sampler to sample the circuit
    sampler = Sampler()
    job = sampler.run(qc)
    result = job.result()
    
    # Extract the quasi-probability distribution
    quasi_dist = result.quasi_dists[0]
    binary_dist = quasi_dist.binary_probabilities()
    
    # Ensure all bitstrings are 3 bits long
    prob_dist = {bitstring.zfill(3): prob for bitstring, prob in binary_dist.items()}
    
    return prob_dist
