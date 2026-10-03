# EVAL_META: task_id=37, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit_aer.primitives import Sampler

def bv_algorithm(s: str):
    n = len(s)
    qc = QuantumCircuit(n + 1, n)
    
    # Initialize the helper qubit in state |->
    qc.x(n)
    qc.h(n)
    
    # Apply Hadamard to all other qubits
    for i in range(n):
        qc.h(i)
        
    # Apply the inner-product oracle (little-endian ordering)
    for i, char in enumerate(reversed(s)):
        if char == '1':
            qc.cx(i, n)
            
    # Apply Hadamard to all other qubits again
    for i in range(n):
        qc.h(i)
        
    # Measure the qubits
    qc.measure(range(n), range(n))
    
    # Run using Aer's Sampler primitive
    sampler = Sampler()
    job = sampler.run(qc)
    result = job.result()
    
    quasi_dist = result.quasi_dists[0]
    bitstrings = list(quasi_dist.binary_probabilities().keys())
    
    return [bitstrings, result]
