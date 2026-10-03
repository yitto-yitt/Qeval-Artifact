# EVAL_META: task_id=53, framework=cirq, class=1
import cirq
from collections import Counter

def xor_gate(a, b):
    # Create 8 qubits
    qubits = [cirq.LineQubit(i) for i in range(8)]
    
    # Convert a and b to binary strings (8 bits)
    a_bin = format(a, '08b')
    b_bin = format(b, '08b')
    
    # Create circuit
    circuit = cirq.Circuit()
    
    # Apply X gates to qubits where corresponding bit in a is 1
    for i, bit in enumerate(a_bin):
        if bit == '1':
            circuit.append(cirq.X(qubits[i]))
    
    # Apply X gates to qubits where corresponding bit in b is 1
    for i, bit in enumerate(b_bin):
        if bit == '1':
            circuit.append(cirq.X(qubits[i]))
    
    # Apply XOR operation: For each position, we want (a_i XOR b_i)
    # Since we already applied X gates for both a and b, the current state represents a^b
    # We just need to measure the qubits
    
    # Measure all qubits
    circuit.append(cirq.measure(*qubits, key='result'))
    
    # Simulate the circuit
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10000)  # Run multiple times to get statistics
    
    # Count the results
    measurements = result.histogram(key='result')
    
    # Normalize to get probabilities
    total_samples = sum(measurements.values())
    prob_dist = {}
    
    for outcome, count in measurements.items():
        # Convert integer outcome to 8-bit binary string
        binary_str = format(outcome, '08b')
        prob_dist[binary_str] = count / total_samples
    
    return prob_dist
