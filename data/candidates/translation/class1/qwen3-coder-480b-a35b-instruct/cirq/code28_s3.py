# EVAL_META: task_id=28, framework=cirq, class=1
import cirq
import numpy as np

def visualize_bell_states():
    # Create qubits
    q0, q1 = cirq.LineQubit.range(2)
    
    # Prepare Phi+ Bell state (|00> + |11>)
    phi_plus_circuit = cirq.Circuit()
    phi_plus_circuit.append(cirq.H(q0))
    phi_plus_circuit.append(cirq.CNOT(q0, q1))
    phi_plus_circuit.append(cirq.measure(q0, q1, key='result'))
    
    # Prepare Phi- Bell state (|00> - |11>)
    phi_minus_circuit = cirq.Circuit()
    phi_minus_circuit.append(cirq.X(q0))
    phi_minus_circuit.append(cirq.H(q0))
    phi_minus_circuit.append(cirq.CNOT(q0, q1))
    phi_minus_circuit.append(cirq.measure(q0, q1, key='result'))
    
    # Simulate both circuits
    simulator = cirq.Simulator()
    
    # Sample results for Phi+
    phi_plus_results = simulator.run(phi_plus_circuit, repetitions=1000)
    phi_plus_measurements = phi_plus_results.measurements['result']
    phi_plus_counts = {}
    for measurement in phi_plus_measurements:
        bitstring = ''.join(map(str, measurement))
        phi_plus_counts[bitstring] = phi_plus_counts.get(bitstring, 0) + 1
    
    # Sample results for Phi-
    phi_minus_results = simulator.run(phi_minus_circuit, repetitions=1000)
    phi_minus_measurements = phi_minus_results.measurements['result']
    phi_minus_counts = {}
    for measurement in phi_minus_measurements:
        bitstring = ''.join(map(str, measurement))
        phi_minus_counts[bitstring] = phi_minus_counts.get(bitstring, 0) + 1
    
    # Calculate probabilities
    phi_plus_total = sum(phi_plus_counts.values())
    phi_minus_total = sum(phi_minus_counts.values())
    
    phi_plus_probs = {key: value / phi_plus_total for key, value in phi_plus_counts.items()}
    phi_minus_probs = {key: value / phi_minus_total for key, value in phi_minus_counts.items()}
    
    return {
        "phi_plus": phi_plus_probs,
        "phi_minus": phi_minus_probs
    }
