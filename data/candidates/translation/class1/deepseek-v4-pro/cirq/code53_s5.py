# EVAL_META: task_id=53, framework=cirq, class=1
import cirq
import numpy as np

def xor_gate(a, b):
    # Define 8 qubits
    qubits = cirq.LineQubit.range(8)
    
    # Initialize qubits to represent input 'a' (little-endian: qubit i holds bit i)
    a_bits = [(a >> i) & 1 for i in range(8)]
    # Initialize qubits to represent input 'b' (apply XOR with b)
    b_bits = [(b >> i) & 1 for i in range(8)]
    
    # Build circuit: start with X gates for a, then X gates for b (XOR operation)
    circuit = cirq.Circuit()
    for i, bit in enumerate(a_bits):
        if bit:
            circuit.append(cirq.X(qubits[i]))
    for i, bit in enumerate(b_bits):
        if bit:
            circuit.append(cirq.X(qubits[i]))
    
    # Measure all qubits
    circuit.append(cirq.measure(*qubits, key='result'))
    
    # Simulate
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    
    # Extract measurement counts
    measurements = result.measurements['result']
    counts = {}
    for sample in measurements:
        # Convert bit array to string (little-endian: qubit 0 is LSB)
        bitstring = ''.join(str(bit) for bit in sample[::-1])
        counts[bitstring] = counts.get(bitstring, 0) + 1
    
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
