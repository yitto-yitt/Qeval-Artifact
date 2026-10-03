# EVAL_META: task_id=31, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.primitives import Sampler


def sampler_qiskit():
    # Create a Bell circuit
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    # Create an Aer simulator with seed 42
    backend = AerSimulator(seed_simulator=42)

    # Create a Sampler instance with the backend
    sampler = Sampler(backend=backend)

    # Run the sampler
    result = sampler.run(qc).result()

    # Get the quasi-probabilities and convert to probabilities
    quasi_dist = result.quasi_dists[0]
    
    # Convert to regular probability distribution dictionary
    prob_dist = {}
    for key, value in quasi_dist.items():
        # Convert integer keys to binary string representation
        bin_str = format(key, f'0{qc.num_clbits}b')
        prob_dist[bin_str] = value

    return prob_dist
