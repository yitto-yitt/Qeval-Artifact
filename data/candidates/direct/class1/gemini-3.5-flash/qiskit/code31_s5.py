# EVAL_META: task_id=31, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler

def sampler_qiskit():
    # Create a Bell circuit
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    # Initialize AerSimulator with seed_simulator=42
    backend = AerSimulator(seed_simulator=42)
    
    # Initialize Qiskit Runtime Sampler with the Aer backend
    sampler = Sampler(backend=backend)
    
    # Run the circuit
    job = sampler.run(qc)
    result = job.result()
    
    # Get the quasi-probability distribution and convert to binary probabilities
    quasi_dist = result.quasi_dists[0]
    prob_dist = quasi_dist.binary_probabilities()
    
    return prob_dist
