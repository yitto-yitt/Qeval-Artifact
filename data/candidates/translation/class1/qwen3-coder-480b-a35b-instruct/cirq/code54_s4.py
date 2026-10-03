# EVAL_META: task_id=54, framework=cirq, class=1
import cirq
from collections import Counter

def and_gate(a, b):
    # Create qubits
    qr_a = [cirq.LineQubit(i) for i in range(3)]
    qr_b = [cirq.LineQubit(i + 3) for i in range(3)]
    ancillary = [cirq.LineQubit(i + 6) for i in range(3)]
    
    circuit = cirq.Circuit()
    
    # Format inputs to 3-bit binary strings
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    # Initialize input qubits based on the bit values
    for i in range(3):
        if a_str[2-i] == '1':
            circuit.append(cirq.X(qr_a[i]))
        if b_str[2-i] == '1':
            circuit.append(cirq.X(qr_b[i]))
    
    # Apply CCX (Toffoli) gates for AND operation
    for i in range(3):
        circuit.append(cirq.TOFFOLI(qr_a[i], qr_b[i], ancillary[i]))
    
    # Measure the ancillary qubits
    circuit.append(cirq.measure(*ancillary, key='result'))
    
    # Simulate the circuit
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10000)  # Run multiple times to get statistics
    
    # Count the results
    measurements = result.histogram(key='result')
    total = sum(measurements.values())
    
    # Convert to probability distribution with 3-bit string keys
    prob_dist = {}
    for outcome, count in measurements.items():
        # Convert integer outcome to 3-bit binary string
        outcome_str = format(outcome, '03b')
        prob_dist[outcome_str] = count / total
    
    return prob_dist
