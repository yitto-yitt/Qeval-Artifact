# EVAL_META: task_id=53, framework=cirq, class=1
import cirq
import numpy as np

def xor_gate(a, b):
    # Create 8 qubits
    qubits = [cirq.LineQubit(i) for i in range(8)]
    
    # Initialize circuit
    circuit = cirq.Circuit()
    
    # Apply X gates to represent input 'a'
    for i in range(8):
        if (a >> i) & 1:
            circuit.append(cirq.X(qubits[7-i]))
    
    # Apply X gates to represent input 'b'
    for i in range(8):
        if (b >> i) & 1:
            circuit.append(cirq.X(qubits[7-i]))
    
    # Perform XOR operation by applying X gates again where both bits were set
    # This effectively computes a XOR b
    result = a ^ b
    
    # Reset the circuit and apply the XOR result directly
    circuit = cirq.Circuit()
    
    # Set up initial state for a
    for i in range(8):
        if (a >> i) & 1:
            circuit.append(cirq.X(qubits[7-i]))
    
    # XOR with b
    for i in range(8):
        if (b >> i) & 1:
            circuit.append(cirq.X(qubits[7-i]))
    
    # Measure all qubits
    circuit.append(cirq.measure(*qubits, key='result'))
    
    # Simulate the circuit
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10000)  # Run multiple times to get distribution
    
    # Count results
    measurements = result.histogram(key='result')
    total_shots = sum(measurements.values())
    
    # Convert to probability distribution
    prob_dist = {}
    for outcome, count in measurements.items():
        # Convert integer outcome to 8-bit binary string
        binary_str = format(outcome, '08b')
        prob_dist[binary_str] = count / total_shots
    
    return prob_dist
