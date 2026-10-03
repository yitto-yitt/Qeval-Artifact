# EVAL_META: task_id=14, framework=cirq, class=1
import cirq
import numpy as np

def bell_each_shot():
    # Create qubits
    q0, q1 = cirq.LineQubit.range(2)
    
    # Create the Bell circuit (Phi+ state: |00> + |11>)
    bell_circuit = cirq.Circuit()
    bell_circuit.append(cirq.H(q0))  # Hadamard on first qubit
    bell_circuit.append(cirq.CNOT(q0, q1))  # CNOT with q0 as control, q1 as target
    bell_circuit.append(cirq.measure(q0, q1, key='result'))  # Measure both qubits
    
    # Simulate the circuit
    simulator = cirq.Simulator()
    result = simulator.run(bell_circuit, repetitions=10)
    
    # Get the measurement results
    measurements = result.measurements['result']
    
    # Count occurrences of each bitstring
    counts = {}
    for measurement in measurements:
        bitstring = ''.join(map(str, measurement))
        counts[bitstring] = counts.get(bitstring, 0) + 1
    
    # Calculate probabilities
    total_shots = 10
    prob_dist = {key: value / total_shots for key, value in counts.items()}
    
    return prob_dist
