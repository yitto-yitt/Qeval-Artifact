# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.primitives import Sampler


def bv_algorithm(s):
    n = len(s)
    
    # Create quantum and classical registers
    qr = QuantumRegister(n + 1)  # n input qubits + 1 ancilla qubit
    cr = ClassicalRegister(n)
    qc = QuantumCircuit(qr, cr)
    
    # Initialize ancilla qubit to |1⟩
    qc.x(qr[n])
    
    # Apply Hadamard gates to all input qubits and ancilla
    for i in range(n + 1):
        qc.h(qr[i])
    
    # Implement the oracle based on the secret string s
    for i in range(n):
        if s[i] == '1':
            qc.cx(qr[i], qr[n])
    
    # Apply Hadamard gates to input qubits again
    for i in range(n):
        qc.h(qr[i])
    
    # Measure the input qubits
    for i in range(n):
        cr[i] = i
        qc.measure(i, i)
    
    # Use Aer simulator
    backend = AerSimulator()
    sampler = Sampler(backend=backend)
    
    # Run the circuit using Sampler
    job = sampler.run([qc])
    result = job.result()
    
    # Extract the quasi-distribution from the results
    quasi_dist = result.quasi_dists[0]
    
    # Convert quasi-distribution to bitstrings and counts
    bitstrings = []
    for outcome, prob in quasi_dist.items():
        # Convert integer outcome to binary string of length n
        bitstring = format(outcome, f'0{n}b')
        # Append according to probability (for demonstration purposes, we just take the most likely outcome)
        # In actual BV algorithm, there should be only one outcome with high probability
        bitstrings.append(bitstring)
        
    # Since BV algorithm should deterministically return the secret string,
    # we can also directly return the expected result
    most_likely_bitstring = sorted(quasi_dist.items(), key=lambda x: x[1], reverse=True)[0][0]
    most_likely_bitstring = format(most_likely_bitstring, f'0{n}b')
    
    # For consistency, return the most probable bitstring as the result
    return [most_likely_bitstring], result
