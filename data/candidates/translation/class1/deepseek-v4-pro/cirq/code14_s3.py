# EVAL_META: task_id=14, framework=cirq, class=1
import cirq
import numpy as np

def bell_each_shot():
    # Create qubits
    q0, q1 = cirq.LineQubit.range(2)
    
    # Build the Bell circuit (phi plus)
    circuit = cirq.Circuit([
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='result')
    ])
    
    # Simulate with 10 shots
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10)
    
    # Get measurement outcomes
    measurements = result.measurements['result']
    
    # Convert bit arrays to strings and count frequencies
    counts = {}
    for bits in measurements:
        bitstring = ''.join(str(b) for b in bits)
        counts[bitstring] = counts.get(bitstring, 0) + 1
    
    # Normalize to probability distribution
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
