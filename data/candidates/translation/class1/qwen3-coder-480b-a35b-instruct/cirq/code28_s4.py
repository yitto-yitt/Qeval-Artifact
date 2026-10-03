# EVAL_META: task_id=28, framework=cirq, class=1
import cirq
import numpy as np

def visualize_bell_states():
    # Create qubits
    q0, q1 = cirq.LineQubit.range(2)
    
    # Prepare |Φ+⟩ Bell state (|00⟩ + |11⟩)/√2
    phi_plus_circuit = cirq.Circuit()
    phi_plus_circuit.append(cirq.H(q0))  # Apply H gate to first qubit
    phi_plus_circuit.append(cirq.CNOT(q0, q1))  # Apply CNOT gate
    
    # Prepare |Φ-⟩ Bell state (|00⟩ - |11⟩)/√2
    phi_minus_circuit = cirq.Circuit()
    phi_minus_circuit.append(cirq.X(q0))  # Apply X gate to first qubit
    phi_minus_circuit.append(cirq.H(q0))  # Apply H gate to first qubit
    phi_minus_circuit.append(cirq.CNOT(q0, q1))  # Apply CNOT gate
    
    # Add measurements to both circuits
    phi_plus_circuit.append(cirq.measure(q0, q1, key='result'))
    phi_minus_circuit.append(cirq.measure(q0, q1, key='result'))
    
    # Simulate both circuits
    simulator = cirq.Simulator()
    
    # Sample results for phi_plus
    phi_plus_results = simulator.run(phi_plus_circuit, repetitions=1000)
    phi_plus_measurements = phi_plus_results.histogram(key='result')
    
    # Sample results for phi_minus
    phi_minus_results = simulator.run(phi_minus_circuit, repetitions=1000)
    phi_minus_measurements = phi_minus_results.histogram(key='result')
    
    # Convert to probability distributions
    total_plus = sum(phi_plus_measurements.values())
    total_minus = sum(phi_minus_measurements.values())
    
    phi_plus_probs = {format(k, '02b'): v / total_plus 
                      for k, v in phi_plus_measurements.items()}
    phi_minus_probs = {format(k, '02b'): v / total_minus 
                       for k, v in phi_minus_measurements.items()}
    
    return {
        "phi_plus": phi_plus_probs,
        "phi_minus": phi_minus_probs
    }
