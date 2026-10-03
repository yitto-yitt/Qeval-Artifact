# EVAL_META: task_id=28, framework=qiskit, class=1

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def visualize_bell_states():
    # Create Phi+ Bell state circuit
    phi_plus_circuit = QuantumCircuit(2, 2)
    phi_plus_circuit.h(0)
    phi_plus_circuit.cx(0, 1)
    phi_plus_circuit.measure([0, 1], [0, 1])
    
    # Create Phi- Bell state circuit
    phi_minus_circuit = QuantumCircuit(2, 2)
    phi_minus_circuit.x(0)
    phi_minus_circuit.h(0)
    phi_minus_circuit.cx(0, 1)
    phi_minus_circuit.measure([0, 1], [0, 1])
    
    # Simulate circuits
    simulator = AerSimulator()
    
    # Transpile circuits
    phi_plus_transpiled = transpile(phi_plus_circuit, simulator)
    phi_minus_transpiled = transpile(phi_minus_circuit, simulator)
    
    # Run simulations
    phi_plus_result = simulator.run(phi_plus_transpiled, shots=1000).result()
    phi_minus_result = simulator.run(phi_minus_transpiled, shots=1000).result()
    
    # Get counts and convert to probability distributions
    phi_plus_counts = phi_plus_result.get_counts()
    phi_minus_counts = phi_minus_result.get_counts()
    
    # Normalize counts to probabilities
    phi_plus_total = sum(phi_plus_counts.values())
    phi_minus_total = sum(phi_minus_counts.values())
    
    phi_plus_probs = {key: value / phi_plus_total for key, value in phi_plus_counts.items()}
    phi_minus_probs = {key: value / phi_minus_total for key, value in phi_minus_counts.items()}
    
    return {
        'phi_plus': phi_plus_probs,
        'phi_minus': phi_minus_probs
    }
