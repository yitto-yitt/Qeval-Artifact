# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np

def init_random_3qubit(desired_vector):
    # Create qubits
    qubits = cirq.LineQubit.range(3)
    
    # Create a simulator
    simulator = cirq.Simulator(seed=42)
    
    # In Cirq, we can use StatePreparationChannel or simply simulate with an initial state.
    # However, to sample it, we can simulate the circuit with the desired_vector as the initial state.
    # We construct a circuit that only contains measurement gates.
    circuit = cirq.Circuit(cirq.measure(*qubits, key='meas'))
    
    # Run the simulation to sample results
    result = simulator.run(circuit, repetitions=1024, initial_state=np.array(desired_vector, dtype=np.complex64))
    
    # Get counts
    # The measurement keys in Cirq return a 2D numpy array of shape (repetitions, num_qubits).
    # We need to convert this to bitstrings.
    measurements = result.measurements['meas']
    counts = {}
    for row in measurements:
        bitstring = ''.join(str(bit) for bit in row)
        counts[bitstring] = counts.get(bitstring, 0) + 1
        
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
