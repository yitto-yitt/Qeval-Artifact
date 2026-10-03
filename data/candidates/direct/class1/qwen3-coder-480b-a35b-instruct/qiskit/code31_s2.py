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

    # Create Aer simulator with seed
    backend = AerSimulator(seed_simulator=42)

    # Create sampler and run
    sampler = Sampler(backend=backend)
    result = sampler.run([qc], shots=1000).result()

    # Get probabilities
    quasi_dist = result.quasi_dists[0]
    
    # Convert to bitstring probabilities
    prob_dict = {}
    for outcome, prob in quasi_dist.items():
        bitstring = format(outcome, '02b')  # Format as 2-bit string
        prob_dict[bitstring] = prob
    
    return prob_dict
