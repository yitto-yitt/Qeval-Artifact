# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator
import numpy as np


def dj_algorithm(oracle):
    # Get the number of qubits from the oracle circuit
    n = oracle.num_qubits - 1  # -1 because last qubit is ancilla/output
    
    # Create quantum registers
    qr = QuantumRegister(n + 1)  # +1 for ancilla qubit
    cr = ClassicalRegister(n)
    
    # Create the full circuit
    qc = QuantumCircuit(qr, cr)
    
    # Initialize ancilla qubit to |1⟩
    qc.x(qr[-1])
    
    # Apply Hadamard to all input qubits and ancilla
    for i in range(n + 1):
        qc.h(qr[i])
    
    # Apply the oracle
    qc.compose(oracle, inplace=True)
    
    # Apply Hadamard to all input qubits again
    for i in range(n):
        qc.h(qr[i])
    
    # Measure the input qubits
    for i in range(n):
        qc.measure(i, i)
    
    # Simulate the circuit
    backend = AerSimulator()
    result = backend.run(qc, shots=1024).result()
    counts = result.get_counts()
    
    # Process counts to ensure all n-bit strings are included
    total_shots = sum(counts.values())
    prob_dist = {}
    
    # Generate all possible n-bit strings
    for i in range(2**n):
        bitstring = format(i, f'0{n}b')
        prob_dist[bitstring] = counts.get(bitstring, 0) / total_shots
    
    return prob_dist
