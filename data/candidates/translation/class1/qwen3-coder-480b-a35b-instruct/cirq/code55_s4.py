# EVAL_META: task_id=55, framework=cirq, class=1
import cirq
from collections import Counter

def or_gate(a, b):
    # Create qubits
    qr_a = [cirq.LineQubit(i) for i in range(3)]
    qr_b = [cirq.LineQubit(i + 3) for i in range(3)]
    ancillary = [cirq.LineQubit(i + 6) for i in range(3)]
    
    circuit = cirq.Circuit()
    
    # Format inputs to 3-bit binary strings
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    # Apply X gates to flip bits that should be 0 (since we want to start with all |1> states)
    for i in range(3):
        if a_str[2-i] == '0':
            circuit.append(cirq.X(qr_a[i]))
        if b_str[2-i] == '0':
            circuit.append(cirq.X(qr_b[i]))
    
    # Apply CCX (Toffoli) gates to compute AND of each bit pair
    for i in range(3):
        circuit.append(cirq.CCX(qr_a[i], qr_b[i], ancillary[i]))
    
    # Apply X gates to ancillary qubits to get OR result (NOT of AND of NOTs - De Morgan's law)
    circuit.append(cirq.X.on_each(*ancillary))
    
    # Add measurements
    circuit.append(cirq.measure(*ancillary, key='result'))
    
    # Simulate the circuit
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10000)
    
    # Count results
    measurements = result.histogram(key='result')
    total = sum(measurements.values())
    
    # Convert to probability distribution
    prob_dist = {}
    for key, count in measurements.items():
        # Convert integer key to 3-bit binary string
        binary_str = format(key, '03b')
        prob_dist[binary_str] = count / total
    
    return prob_dist
