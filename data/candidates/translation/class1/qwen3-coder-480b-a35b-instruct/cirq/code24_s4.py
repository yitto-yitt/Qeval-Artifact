# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np

def dj_algorithm(oracle):
    n = len(oracle.all_qubits())
    qubits = cirq.LineQubit.range(n)
    
    # Extract the number of input qubits (all except the last one which is the output)
    num_input_qubits = n - 1
    
    circuit = cirq.Circuit()
    
    # Apply X to the last qubit (output qubit)
    circuit.append(cirq.X(qubits[-1]))
    
    # Apply H to all qubits
    circuit.append(cirq.H.on_each(*qubits))
    
    # Append the oracle
    circuit.append(oracle)
    
    # Apply H to all qubits again
    circuit.append(cirq.H.on_each(*qubits))
    
    # Measure only the input qubits
    circuit.append(cirq.measure(*qubits[:-1], key='result'))
    
    # Simulate the circuit
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=8192)  # Standard number of repetitions
    
    # Count the results
    measurements = result.records['result'][0]  # Shape: (repetitions, num_input_qubits)
    
    # Count occurrences of each bitstring
    counts = {}
    for i in range(len(measurements)):
        bitstring = ''.join(map(str, measurements[i]))
        if bitstring in counts:
            counts[bitstring] += 1
        else:
            counts[bitstring] = 1
    
    # Normalize to get probabilities
    total = sum(counts.values())
    prob_dist = {key: value / total for key, value in counts.items()}
    
    return prob_dist
