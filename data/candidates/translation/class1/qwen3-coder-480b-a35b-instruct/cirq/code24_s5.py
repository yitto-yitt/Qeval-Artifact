# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np

def dj_algorithm(oracle):
    n = len(oracle.all_qubits())
    qubits = cirq.LineQubit.range(n)
    
    # Extract the number of input qubits (all except the last one which is the output)
    num_input_qubits = n - 1
    
    circuit = cirq.Circuit()
    
    # Initialize the last qubit to |1⟩ by applying X gate
    circuit.append(cirq.X(qubits[-1]))
    
    # Apply Hadamard to all qubits
    circuit.append(cirq.H.on_each(*qubits))
    
    # Append the oracle
    circuit.append(oracle)
    
    # Apply Hadamard to all qubits again
    circuit.append(cirq.H.on_each(*qubits))
    
    # Measure the first n-1 qubits (input register)
    circuit.append(cirq.measure(*qubits[:-1], key='result'))
    
    # Simulate the circuit
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=8192)  # Standard number of repetitions
    
    # Count the measurement results
    measurements = result.histogram(key='result')
    
    # Calculate probabilities
    total_measurements = sum(measurements.values())
    prob_dist = {}
    
    for outcome, count in measurements.items():
        # Convert integer outcome to binary string with appropriate length
        binary_str = format(outcome, f'0{num_input_qubits}b')
        prob_dist[binary_str] = count / total_measurements
    
    return prob_dist
