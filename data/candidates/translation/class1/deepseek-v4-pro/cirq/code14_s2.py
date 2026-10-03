# EVAL_META: task_id=14, framework=cirq, class=1
import cirq
import numpy as np

def bell_each_shot():
    # Create qubits
    q0, q1 = cirq.LineQubit.range(2)
    
    # Build the phi plus Bell circuit
    circuit = cirq.Circuit([
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='result')
    ])
    
    # Use the Cirq simulator
    simulator = cirq.Simulator()
    
    # Run the circuit for 10 shots
    result = simulator.run(circuit, repetitions=10)
    
    # Extract measurement results
    measurements = result.measurements['result']
    
    # Count occurrences of each bitstring
    counts = {}
    for bits in measurements:
        bitstring = ''.join(str(b) for b in bits)
        counts[bitstring] = counts.get(bitstring, 0) + 1
    
    # Return probability distribution
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
