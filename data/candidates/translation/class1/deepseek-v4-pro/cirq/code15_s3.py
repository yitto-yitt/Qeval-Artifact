# EVAL_META: task_id=15, framework=cirq, class=1
import cirq
import numpy as np

def noisy_bell():
    # Create the Bell circuit
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit([
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='result')
    ])
    
    # Use a noise model to simulate a noisy device
    # Since we can't use FakeBelemV2 directly, we simulate with depolarizing noise
    # to mimic the behavior of a real device
    noise = cirq.depolarize(0.01)
    noisy_circuit = circuit.with_noise(noise)
    
    # Simulate with 1000 shots
    simulator = cirq.Simulator()
    result = simulator.run(noisy_circuit, repetitions=1000)
    
    # Get counts and convert to probability distribution
    counts = result.histogram(key='result')
    total = sum(counts.values())
    
    # Convert integer keys to bitstrings
    prob_dist = {}
    for k, v in counts.items():
        bitstring = format(k, '02b')
        prob_dist[bitstring] = v / total
    
    return prob_dist
