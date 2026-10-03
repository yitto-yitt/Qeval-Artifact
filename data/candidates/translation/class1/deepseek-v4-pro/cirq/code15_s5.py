# EVAL_META: task_id=15, framework=cirq, class=1
import cirq
import numpy as np

def noisy_bell():
    # Build Bell circuit
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit([
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='result'),
    ])

    # Use a depolarizing noise model to approximate a noisy backend
    noise = cirq.depolarize(0.01)
    simulator = cirq.DensityMatrixSimulator(noise=noise)

    # Run the circuit with 1000 shots
    result = simulator.run(circuit, repetitions=1000)
    counts = result.histogram(key='result')

    # Convert to bitstring dict and normalize to probabilities
    total = sum(counts.values())
    return {format(k, '02b'): v / total for k, v in counts.items()}
