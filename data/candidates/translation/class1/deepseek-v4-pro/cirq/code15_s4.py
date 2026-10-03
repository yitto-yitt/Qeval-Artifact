# EVAL_META: task_id=15, framework=cirq, class=1
import cirq
import numpy as np

def noisy_bell():
    # Create Bell circuit
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit([
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='meas')
    ])
    
    # Simulate with noise model approximating a real backend
    # Using a depolarizing noise model as a simplified fake backend approximation
    noise_model = cirq.ConstantQubitNoiseModel(cirq.depolarize(0.001))
    simulator = cirq.DensityMatrixSimulator(noise=noise_model)
    
    # Run the circuit
    result = simulator.run(circuit, repetitions=1000)
    
    # Get measurement results
    measurements = result.measurements['meas']
    counts = {}
    for bits in measurements:
        bitstring = ''.join(str(b) for b in bits)
        counts[bitstring] = counts.get(bitstring, 0) + 1
    
    # Convert to probability distribution
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
