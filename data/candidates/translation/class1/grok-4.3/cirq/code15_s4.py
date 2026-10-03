# EVAL_META: task_id=15, framework=cirq, class=1
import cirq

def noisy_bell():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='meas')
    )
    noisy_circuit = circuit.with_noise(cirq.depolarize(0.01))
    simulator = cirq.Simulator()
    result = simulator.run(noisy_circuit, repetitions=1000)
    samples = result.measurements['meas']
    counts = {}
    for sample in samples:
        bits = ''.join(str(b) for b in sample)
        counts[bits] = counts.get(bits, 0) + 1
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
