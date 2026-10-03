# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
from collections import Counter

def dj_algorithm(oracle):
    n = len(oracle.all_qubits())
    qubits = sorted(oracle.all_qubits())
    input_qubits = qubits[:-1]
    output_qubit = qubits[-1]
    
    circuit = cirq.Circuit()
    
    # Initialize output qubit to |1>
    circuit.append(cirq.X(output_qubit))
    
    # Apply Hadamard to all qubits
    circuit.append(cirq.H.on_each(*qubits))
    
    # Apply oracle
    circuit.append(oracle)
    
    # Apply Hadamard to all qubits again
    circuit.append(cirq.H.on_each(*qubits))
    
    # Measure input qubits
    circuit.append(cirq.measure(*input_qubits, key='result'))
    
    # Run simulation
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10000)
    measurements = result.measurements['result']
    
    # Convert to bitstrings and count
    counts = Counter()
    for measurement in measurements:
        bitstring = ''.join(str(bit) for bit in measurement)
        counts[bitstring] += 1
    
    # Normalize to probabilities
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
