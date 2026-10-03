# EVAL_META: task_id=54, framework=cirq, class=1
import cirq
from collections import Counter

def and_gate(a, b):
    # Create qubits
    qr_a = [cirq.LineQubit(i) for i in range(3)]
    qr_b = [cirq.LineQubit(i + 3) for i in range(3)]
    ancillary = [cirq.LineQubit(i + 6) for i in range(3)]
    
    # Convert inputs to binary strings
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    # Create circuit
    circuit = cirq.Circuit()
    
    # Initialize input qubits based on a and b
    for i in range(3):
        if a_bin[2-i] == '1':
            circuit.append(cirq.X(qr_a[i]))
        if b_bin[2-i] == '1':
            circuit.append(cirq.X(qr_b[i]))
    
    # Apply CCX (Toffoli) gates to compute AND
    for i in range(3):
        circuit.append(cirq.CCX(qr_a[i], qr_b[i], ancillary[i]))
    
    # Measure the ancillary qubits
    circuit.append(cirq.measure(*ancillary, key='result'))
    
    # Simulate the circuit
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=8192)  # Standard number of repetitions
    
    # Process results
    measurements = result.measurements['result']
    # Convert measurements to bitstrings
    bitstrings = []
    for meas in measurements:
        bitstring = ''.join(str(bit) for bit in meas)
        bitstrings.append(bitstring)
    
    # Count occurrences
    counts = Counter(bitstrings)
    total = sum(counts.values())
    
    # Calculate probabilities
    prob_dist = {key: value / total for key, value in counts.items()}
    
    return prob_dist
