# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator
import numpy as np


def dj_algorithm(oracle):
    # Get the number of qubits from the oracle circuit
    n = oracle.num_qubits - 1  # -1 because last qubit is ancilla/output
    
    # Create quantum registers
    qr_input = QuantumRegister(n, 'input')
    qr_ancilla = QuantumRegister(1, 'ancilla')
    cr = ClassicalRegister(n, 'c')
    
    # Create the full circuit
    qc = QuantumCircuit(qr_input, qr_ancilla, cr)
    
    # Initialize ancilla to |1> state
    qc.x(qr_ancilla[0])
    
    # Apply Hadamard to all input qubits and the ancilla
    for i in range(n):
        qc.h(qr_input[i])
    qc.h(qr_ancilla[0])
    
    # Apply the oracle
    qc.compose(oracle, inplace=True)
    
    # Apply Hadamard to all input qubits again
    for i in range(n):
        qc.h(qr_input[i])
    
    # Measure the input register
    for i in range(n):
        qc.measure(qr_input[i], cr[i])
    
    # Simulate the circuit
    backend = AerSimulator()
    result = backend.run(qc, shots=1024).result()
    counts = result.get_counts(qc)
    
    # Return the probability distribution
    total_shots = sum(counts.values())
    prob_dist = {bitstring: count / total_shots for bitstring, count in counts.items()}
    
    return prob_dist
