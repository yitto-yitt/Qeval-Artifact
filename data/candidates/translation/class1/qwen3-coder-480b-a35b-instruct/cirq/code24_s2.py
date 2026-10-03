# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np

def dj_algorithm(oracle):
    n = len(oracle.all_qubits())
    qubits = cirq.LineQubit.range(n)
    
    # Extract the number of input qubits (all except the last one which is the output)
    num_input_qubits = n - 1
    
    circuit = cirq.Circuit()
    
    # Apply X to the last (output) qubit
    circuit.append(cirq.X(qubits[-1]))
    
    # Apply H to all qubits
    circuit.append(cirq.H.on_each(*qubits))
    
    # Add the oracle
    circuit.append(oracle)
    
    # Apply H to all qubits again
    circuit.append(cirq.H.on_each(*qubits))
    
    # Measure the first n-1 qubits (input register)
    circuit.append(cirq.measure(*qubits[:num_input_qubits], key='result'))
    
    # Simulate the circuit
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=8192)  # Standard number of repetitions
    
    # Count the results
    measurements = result.measurements['result']
    counts = {}
    for measurement in measurements:
        bitstring = ''.join(map(str, measurement))
        counts[bitstring] = counts.get(bitstring, 0) + 1
    
    # Convert to probability distribution
    total = sum(counts.values())
    prob_dist = {key: value / total for key, value in counts.items()}
    
    return prob_dist
