# EVAL_META: task_id=37, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit_aer import Sampler

def bv_algorithm(s):
    n = len(s)
    qc = QuantumCircuit(n + 1, n)
    
    # Put auxiliary qubit in state |->
    qc.x(n)
    qc.h(n)
    
    # Apply Hadamard gates to input qubits
    for i in range(n):
        qc.h(i)
        
    qc.barrier()
    
    # Apply Oracle
    for i, char in enumerate(reversed(s)):
        if char == '1':
            qc.cx(i, n)
            
    qc.barrier()
    
    # Apply Hadamard gates to input qubits again
    for i in range(n):
        qc.h(i)
        
    # Measure input qubits
    for i in range(n):
        qc.measure(i, i)
        
    # Run using Aer Sampler
    sampler = Sampler()
    result = sampler.run(qc).result()
    
    # Extract bitstrings
    try:
        quasi_dist = result.quasi_dists[0]
        bitstrings = {format(k, f'0{n}b'): v for k, v in quasi_dist.items()}
    except AttributeError:
        # Fallback for V2 sampler if encountered
        pub_result = result[0]
        creg_name = qc.cregs[0].name
        counts = getattr(pub_result.data, creg_name).get_counts()
        total = sum(counts.values())
        bitstrings = {k: v / total for k, v in counts.items()}
        
    return [bitstrings, result]
