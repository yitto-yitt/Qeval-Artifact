# EVAL_META: task_id=37, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit_aer.primitives import Sampler

def bv_algorithm(s: str):
    n = len(s)
    qc = QuantumCircuit(n + 1, n)
    
    # Initialize auxiliary qubit to |->
    qc.x(n)
    qc.h(n)
    
    # Apply Hadamard to input qubits
    for i in range(n):
        qc.h(i)
        
    # Apply Oracle
    for i in range(n):
        if s[n - 1 - i] == '1':
            qc.cx(i, n)
            
    # Apply Hadamard to input qubits again
    for i in range(n):
        qc.h(i)
        
    # Measure input qubits
    qc.measure(range(n), range(n))
    
    # Run using Aer Sampler
    sampler = Sampler()
    job = sampler.run(qc)
    result = job.result()
    
    # Extract bitstrings
    quasi_dist = result.quasi_dists[0]
    binary_probs = quasi_dist.binary_probabilities()
    bitstrings = list(binary_probs.keys())
    
    return [bitstrings, result]
