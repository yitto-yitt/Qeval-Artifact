# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer.primitives import Sampler

def bv_algorithm(s: str):
    n = len(s)
    qc = QuantumCircuit(n + 1, n)
    
    # Put auxiliary qubit in state |->
    qc.x(n)
    qc.h(range(n + 1))
    qc.barrier()
    
    # Apply Oracle (mapping s to the qubits)
    for i in range(n):
        if s[n - 1 - i] == '1':
            qc.cx(i, n)
    qc.barrier()
    
    # Apply Hadamard to input qubits and measure
    qc.h(range(n))
    qc.measure(range(n), range(n))
    
    # Run using Aer Sampler
    sampler = Sampler()
    result = sampler.run(qc).result()
    
    # Extract bitstrings with their quasi-probabilities
    quasi_dist = result.quasi_dists[0]
    bitstrings = quasi_dist.binary_probabilities()
    
    return [bitstrings, result]
