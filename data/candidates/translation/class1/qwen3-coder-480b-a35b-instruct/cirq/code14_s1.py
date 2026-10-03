# EVAL_META: task_id=14, framework=cirq, class=1
import cirq
import collections

def bell_each_shot():
    # Create quantum and classical registers
    qubits = [cirq.LineQubit(i) for i in range(2)]
    
    # Build the circuit
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.measure(*qubits, key='result'))
    
    # Run the simulation
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10)
    
    # Process results
    measurements = result.measurements['result']
    bitstrings = [''.join(map(str, row)) for row in measurements]
    counts = collections.Counter(bitstrings)
    
    # Convert to probability distribution
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
