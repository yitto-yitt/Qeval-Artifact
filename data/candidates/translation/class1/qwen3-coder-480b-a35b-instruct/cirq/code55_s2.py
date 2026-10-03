# EVAL_META: task_id=55, framework=cirq, class=1
import cirq
from collections import Counter

def or_gate(a, b):
    # Create qubits
    qr_a = [cirq.LineQubit(i) for i in range(3)]
    qr_b = [cirq.LineQubit(i + 3) for i in range(3)]
    ancillary = [cirq.LineQubit(i + 6) for i in range(3)]
    
    circuit = cirq.Circuit()
    
    # Format inputs to binary
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    # Initialize input qubits - flip if bit is 0 (to simulate classical OR with proper logic)
    for i in range(3):
        if a_bin[2-i] == '0':
            circuit.append(cirq.X(qr_a[i]))
        if b_bin[2-i] == '0':
            circuit.append(cirq.X(qr_b[i]))
    
    # Apply Toffoli gates (CCX equivalent in Cirq)
    for i in range(3):
        circuit.append(cirq.TOFFOLI(qr_a[i], qr_b[i], ancillary[i]))
    
    # Flip all ancilla qubits
    circuit.append(cirq.X.on_each(*ancillary))
    
    # Measure ancilla qubits
    circuit.append(cirq.measure(*ancillary, key='result'))
    
    # Simulate the circuit
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10000)  # Run multiple times to get probability distribution
    
    # Get measurement results
    measurements = result.measurements['result']
    
    # Count occurrences of each outcome
    counts = Counter()
    for measurement in measurements:
        # Convert measurement array to string
        outcome_str = ''.join(map(str, measurement))
        counts[outcome_str] += 1
    
    # Calculate probabilities
    total = sum(counts.values())
    prob_dist = {outcome: count / total for outcome, count in counts.items()}
    
    return prob_dist
