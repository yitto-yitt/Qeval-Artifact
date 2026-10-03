# EVAL_META: task_id=15, framework=cirq, class=1
import cirq
from collections import Counter

def noisy_bell():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='result')
    )
    noise = cirq.depolarize(p=0.02)
    noisy_circuit = circuit.with_noise(noise)
    simulator = cirq.Simulator()
    result = simulator.run(noisy_circuit, repetitions=1000)
    measurements = result.measurements['result']
    bitstrings = [''.join(map(str, row[::-1])) for row in measurements]
    counts = Counter(bitstrings)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
