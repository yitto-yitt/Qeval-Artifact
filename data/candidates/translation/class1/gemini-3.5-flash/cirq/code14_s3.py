# EVAL_META: task_id=14, framework=cirq, class=1
import cirq
from collections import Counter

def bell_each_shot():
    # Create qubits
    q0, q1 = cirq.LineQubit.range(2)
    
    # Create circuit
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.CNOT(q0, q1))
    circuit.append(cirq.measure(q0, q1, key='meas'))
    
    # Simulate the circuit for 10 shots
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10)
    
    # Extract measurements and convert to Qiskit-style MSB-first bitstrings
    measurements = result.measurements['meas']
    bitstrings = ["".join(str(x) for x in row[::-1]) for row in measurements]
    
    # Calculate probability distribution
    counts = Counter(bitstrings)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
