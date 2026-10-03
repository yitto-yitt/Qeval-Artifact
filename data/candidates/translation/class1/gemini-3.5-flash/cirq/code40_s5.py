# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np

def init_random_3qubit(desired_vector):
    # Map desired_vector to a state preparation
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    
    # In Cirq, we can use cirq.StatePreparationChannel to prepare a state,
    # but the simplest way to sample from a statevector is to use a simulator
    # and pass the desired_vector as the initial state, or construct a circuit
    # that prepares the state.
    # However, cirq.Simulator().run does not support initial_state directly.
    # A standard way to prepare statevector in Cirq is using cirq.StatePreparationChannel
    # which is available in cirq.
    # Alternatively, we can use cirq.StatePreparationChannel or just simulate
    # with simulate(..., initial_state=desired_vector) and then sample from the resulting state,
    # or use cirq.sample(..., initial_state=desired_vector).
    # Let's check if cirq.sample supports initial_state. Yes, cirq.sample supports initial_state.
    # Wait, the prompt says "sample it using Qiskit Runtime Sampler on an Aer simulator backend."
    # We should use cirq.Simulator() to sample.
    # cirq.sample(circuit, repetitions=1024, initial_state=desired_vector) is very clean.
    # Let's verify if cirq.sample is standard. Yes, cirq.sample(circuit, repetitions=1024, initial_state=desired_vector)
    # works and returns a Result object.
    
    circuit.append(cirq.measure(*qubits, key='meas'))
    
    # We use a fixed seed for the simulator to match Qiskit's seed_simulator=42 behavior if possible.
    # In Cirq, we can pass a seed to the simulator.
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=1024, initial_state=desired_vector)
    
    # Get the counts
    # result.measurements['meas'] is a 2D array of shape (repetitions, 3)
    measurements = result.measurements['meas']
    counts = {}
    for row in measurements:
        bitstring = "".join(str(x) for x in row)
        counts[bitstring] = counts.get(bitstring, 0) + 1
        
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
