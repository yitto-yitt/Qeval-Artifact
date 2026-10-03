# EVAL_META: task_id=15, framework=cirq, class=1
import cirq
import cirq.contrib.noise_models as noise_models
import numpy as np
from collections import Counter

def noisy_bell():
    # Create the Bell circuit
    q0, q1 = cirq.LineQubit.range(2)
    bell_circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='meas')
    )
    
    # Create a noise model based on a depolarizing gate (approximating the fake backend noise)
    noise_model = noise_models.depolarizing_noise(0.001)
    
    # Add noise to the circuit
    noisy_circuit = cirq.Circuit()
    for moment in bell_circuit:
        noisy_moment = []
        for op in moment:
            noisy_moment.append(op)
            if not isinstance(op.gate, cirq.MeasurementGate):
                # Apply noise after each non-measurement gate
                noisy_moment.extend(noise_model.noisy_operation(op).operations)
        noisy_circuit.append(noisy_moment)
    
    # Run the simulation
    simulator = cirq.DensityMatrixSimulator()
    result = simulator.run(noisy_circuit, repetitions=1000)
    
    # Extract measurements and compute probabilities
    measurements = result.measurements['meas']
    bitstrings = ["".join(map(str, row)) for row in measurements]
    counts = Counter(bitstrings)
    
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
