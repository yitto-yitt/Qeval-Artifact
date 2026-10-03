# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np

def init_random_3qubit(desired_vector):
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    
    # Normalize the desired vector
    normalized_vector = np.array(desired_vector) / np.linalg.norm(desired_vector)
    
    # Create a state preparation circuit
    circuit.append(cirq.StatePreparationChannel(normalized_vector).on(*qubits))
    circuit.append(cirq.measure(*qubits, key='meas'))
    
    # Run simulation
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=10000)
    
    # Extract measurements and compute probabilities
    measurements = result.measurements['meas']
    bitstrings = ["".join(map(str, row)) for row in measurements]
    unique, counts = np.unique(bitstrings, return_counts=True)
    
    # Convert to dictionary with binary string keys
    prob_dict = {bitstring: count/len(bitstrings) for bitstring, count in zip(unique, counts)}
    return prob_dict
