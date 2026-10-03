# EVAL_META: task_id=53, framework=qiskit, class=1

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
import numpy as np

def xor_gate(a, b):
    # Convert inputs to 8-bit binary strings
    a_bits = format(a, '08b')
    b_bits = format(b, '08b')
    
    # Create quantum circuit with 8 qubits for each input and 8 for output
    qreg_a = QuantumRegister(8, 'a')
    qreg_b = QuantumRegister(8, 'b')
    qreg_out = QuantumRegister(8, 'out')
    creg = ClassicalRegister(8, 'c')
    qc = QuantumCircuit(qreg_a, qreg_b, qreg_out, creg)
    
    # Initialize the first two registers with the input values
    for i in range(8):
        if a_bits[i] == '1':
            qc.x(qreg_a[i])
        if b_bits[i] == '1':
            qc.x(qreg_b[i])
    
    # Apply XOR operation: out[i] = a[i] XOR b[i]
    for i in range(8):
        qc.cx(qreg_a[i], qreg_out[i])
        qc.cx(qreg_b[i], qreg_out[i])
    
    # Measure the output register
    for i in range(8):
        qc.measure(qreg_out[i], creg[i])
    
    # Simulate the circuit
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    result = simulator.run(compiled_circuit, shots=1000).result()
    counts = result.get_counts()
    
    # Normalize to get probability distribution
    total_shots = sum(counts.values())
    prob_dist = {key: value / total_shots for key, value in counts.items()}
    
    return prob_dist
