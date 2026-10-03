# EVAL_META: task_id=55, framework=cirq, class=1
import cirq
import collections

def or_gate(a, b):
    # Create qubits
    qr_a = [cirq.LineQubit(i) for i in range(3)]
    qr_b = [cirq.LineQubit(i) for i in range(3, 6)]
    ancillary = [cirq.LineQubit(i) for i in range(6, 9)]
    
    # Create circuit
    circuit = cirq.Circuit()
    
    # Convert inputs to binary strings
    a_bits = format(a, '03b')
    b_bits = format(b, '03b')
    
    # Initialize inputs (X gates for 0 bits)
    for i in range(3):
        if a_bits[2-i] == '0':
            circuit.append(cirq.X(qr_a[i]))
        if b_bits[2-i] == '0':
            circuit.append(cirq.X(qr_b[i]))
    
    # Implement OR gate using CCX and X gates
    for i in range(3):
        circuit.append(cirq.CCX(qr_a[i], qr_b[i], ancillary[i]))
    
    # Flip ancillary qubits to get OR result
    circuit.append(cirq.X.on_each(*ancillary))
    
    # Measure ancillary qubits
    circuit.append(cirq.measure(*ancillary, key='result'))
    
    # Run simulation
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10000)
    
    # Get measurement results
    measurements = result.measurements['result']
    counts = collections.Counter([''.join(map(str, row)) for row in measurements])
    
    # Normalize to probabilities
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
