# EVAL_META: task_id=28, framework=cirq, class=1
import cirq
import collections

def visualize_bell_states():
    # Create qubits
    q0, q1 = cirq.LineQubit.range(2)
    
    # Phi plus circuit
    phi_plus_circuit = cirq.Circuit()
    phi_plus_circuit.append(cirq.H(q0))
    phi_plus_circuit.append(cirq.CNOT(q0, q1))
    phi_plus_circuit.append(cirq.measure(q0, q1, key='result'))
    
    # Phi minus circuit
    phi_minus_circuit = cirq.Circuit()
    phi_minus_circuit.append(cirq.X(q0))
    phi_minus_circuit.append(cirq.H(q0))
    phi_minus_circuit.append(cirq.CNOT(q0, q1))
    phi_minus_circuit.append(cirq.measure(q0, q1, key='result'))
    
    # Simulate circuits
    simulator = cirq.Simulator()
    phi_plus_result = simulator.run(phi_plus_circuit, repetitions=1000)
    phi_minus_result = simulator.run(phi_minus_circuit, repetitions=1000)
    
    # Extract measurements and convert to bitstrings
    phi_plus_measurements = [''.join(map(str, result)) for result in phi_plus_result.measurements['result']]
    phi_minus_measurements = [''.join(map(str, result)) for result in phi_minus_result.measurements['result']]
    
    # Count occurrences
    phi_plus_counts = collections.Counter(phi_plus_measurements)
    phi_minus_counts = collections.Counter(phi_minus_measurements)
    
    # Normalize to probabilities
    phi_plus_total = sum(phi_plus_counts.values())
    phi_minus_total = sum(phi_minus_counts.values())
    
    phi_plus_probs = {key: value / phi_plus_total for key, value in phi_plus_counts.items()}
    phi_minus_probs = {key: value / phi_minus_total for key, value in phi_minus_counts.items()}
    
    return {
        "phi_plus": phi_plus_probs,
        "phi_minus": phi_minus_probs
    }
