# EVAL_META: task_id=15, framework=cirq, class=1
import cirq
import numpy as np
from cirq.contrib.noise_models import NoiseModel
from cirq.devices.noise_properties import NoisePropertiesFromNoiseModel

def noisy_bell():
    # Create Bell circuit
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit([
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='result')
    ])

    # Simulate with a noisy model that mimics a realistic backend
    # FakeBelemV2-like noise: depolarizing and readout errors
    noise_model = NoiseModel(
        depolarizing_error=0.001,
        readout_error=0.01,
    )

    simulator = cirq.DensityMatrixSimulator(noise=noise_model)

    # Run with shots
    result = simulator.run(circuit, repetitions=1000)

    # Get counts and normalize to probabilities
    hist = result.histogram(key='result')
    total = sum(hist.values())
    # Convert to bitstrings
    counts = {}
    for outcome, count in hist.items():
        bitstring = format(outcome, '02b')
        counts[bitstring] = count

    return {key: value / total for key, value in counts.items()}
