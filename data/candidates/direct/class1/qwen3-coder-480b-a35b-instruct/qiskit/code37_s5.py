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
            qc.cx(qr[i], qr[n])  # CNOT gate from input qubit i to ancilla
    
    # Apply Hadamard gates to input qubits again
    for i in range(n):
        qc.h(qr[i])
    
    # Measure the input qubits
    for i in range(n):
        cr[i] = i
    qc.measure(range(n), range(n))
    
    # Execute the circuit using Sampler
    sampler = Sampler(backend=AerSimulator())
    result = sampler.run([qc]).result()
    
    # Extract the bitstrings from the results
    # Since BV algorithm should deterministically return the secret string,
    # we expect mostly one outcome
    quasi_dist = result.quasi_dists[0]
    bitstrings = []
    for bitstring_int in quasi_dist:
        bitstring = format(bitstring_int, f'0{n}b')
        # Convert to list format as requested
        bitstrings.extend([bitstring] * int(quasi_dist[bitstring_int] * 1000))  # Approximate sampling
    
    # Most common result should be the secret string
    most_common_bitstring_int = max(quasi_dist, key=quasi_dist.get)
    most_common_bitstring = format(most_common_bitstring_int, f'0{n}b')
    
    # For deterministic algorithm like BV, just return the correct answer
    bitstrings = [most_common_bitstring]  # Since BV is deterministic, we expect the correct answer
    
    return [bitstrings, result]
