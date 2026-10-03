# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np

def init_random_3qubit(desired_vector):
    # Create 3 qubits
    qubits = cirq.LineQubit.range(3)
    
    # Create a circuit
    circuit = cirq.Circuit()
    
    # Initialize the state using StatePreparationChannel or by applying a custom gate.
    # In Cirq, we can use cirq.StatePreparationChannel to prepare a state.
    # Wait, cirq.StatePreparationChannel is available in cirq.
    # Let's check if cirq.StatePreparationChannel exists. Yes, cirq.StatePreparationChannel(desired_vector) is a gate.
    # It can be applied to the qubits.
    state_prep = cirq.StatePreparationChannel(desired_vector)
    circuit.append(state_prep.on(*qubits))
    
    # Measure all qubits
    circuit.append(cirq.measure(*qubits, key='meas'))
    
    # Simulate the circuit using cirq.Simulator
    # To match the seed_simulator=42, we can pass a seed to the Simulator.
    simulator = cirq.Simulator(seed=42)
    
    # Run the simulation. We need to sample it.
    # The Qiskit code uses Sampler which by default does 1024 shots.
    # Let's use 1024 repetitions.
    result = simulator.run(circuit, repetitions=1024)
    
    # Get the counts
    # result.histogram(key='meas') returns a collections.Counter of int to count.
    # We need to convert the integer keys to bitstrings of length 3.
    histogram = result.histogram(key='meas')
    total = sum(histogram.values())
    
    counts = {}
    for val, count in histogram.items():
        # Format val as a binary string of length 3
        bitstring = format(val, '03b')
        counts[bitstring] = count / total
        
    return counts
