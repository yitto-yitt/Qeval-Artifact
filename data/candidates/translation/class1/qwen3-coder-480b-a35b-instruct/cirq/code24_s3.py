# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np

def dj_algorithm(oracle):
    n = len(oracle.all_qubits())
    qubits = list(cirq.LineQubit.range(n))
    
    # Create circuit
    circuit = cirq.Circuit()
    
    # Apply X gate to the last qubit (output qubit)
    circuit.append(cirq.X(qubits[-1]))
    
    # Apply H gates to all qubits
    circuit.append(cirq.H.on_each(*qubits))
    
    # Add the oracle
    circuit.append(oracle)
    
    # Apply H gates again to all qubits
    circuit.append(cirq.H.on_each(*qubits))
    
    # Measure all qubits except the last one (input register)
    circuit.append(cirq.measure(*qubits[:-1], key='result'))
    
    # Simulate the circuit
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=8192)  # Standard number of repetitions
    
    # Count the measurement results
    measurements = result.histogram(key='result')
    
    # Calculate probabilities
    total_measurements = sum(measurements.values())
    prob_dist = {}
    
    for key, count in measurements.items():
        # Convert integer key to binary string with appropriate length
        binary_str = format(key, f'0{n-1}b')
        prob_dist[binary_str] = count / total_measurements
    
    return prob_dist
