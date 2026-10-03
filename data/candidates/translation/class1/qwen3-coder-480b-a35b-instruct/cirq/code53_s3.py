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
    
    # Perform XOR operation by applying CNOT gates to copy the XOR result
    # We'll just apply the inputs and measure - since XOR is a classical operation,
    # we can simulate it by having the initial state represent a, then adding b
    # Actually, let's implement XOR properly using quantum operations
    
    # Reset circuit and implement properly
    circuit = cirq.Circuit()
    
    # Prepare initial state representing 'a'
    for i in range(8):
        if (a >> i) & 1:
            circuit.append(cirq.X(qubits[7-i]))
    
    # XOR 'b' with current state (which is 'a')
    for i in range(8):
        if (b >> i) & 1:
            circuit.append(cirq.X(qubits[7-i]))
    
    # Measure all qubits
    circuit.append(cirq.measure(*qubits, key='result'))
    
    # Simulate the circuit
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)  # Run multiple times to get statistics
    
    # Count the results
    measurements = result.measurements['result']
    counts = {}
    for meas in measurements:
        # Convert the measurement array to a binary string
        binary_str = ''.join(map(str, meas[::-1]))  # Reverse to get MSB on left
        if binary_str in counts:
            counts[binary_str] += 1
        else:
            counts[binary_str] = 1
    
    # Calculate probabilities
    total = sum(counts.values())
    prob_dist = {key: value / total for key, value in counts.items()}
    
    return prob_dist
