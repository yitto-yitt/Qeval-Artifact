# EVAL_META: task_id=14, framework=cirq, class=1
import cirq
from collections import Counter

def bell_each_shot():
    # Create a quantum circuit with 2 qubits
    qubits = [cirq.LineQubit(i) for i in range(2)]
    circuit = cirq.Circuit()
    
    # Apply gates: H on first qubit, then CNOT
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.CX(qubits[0], qubits[1]))
    
    # Measure both qubits
    circuit.append(cirq.measure(*qubits, key='result'))
    
    # Simulate the circuit 10 times
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10)
    
    # Get the measurements
    measurements = result.measurements['result']
    
    # Convert measurements to bitstrings
    bitstrings = []
    for measurement in measurements:
        bitstring = ''.join(map(str, measurement))
        bitstrings.append(bitstring)
    
    # Count occurrences of each bitstring
    counts = Counter(bitstrings)
    
    # Calculate probabilities
    total = sum(counts.values())
    prob_dist = {key: value / total for key, value in counts.items()}
    
    return prob_dist
