# EVAL_META: task_id=15, framework=cirq, class=1
import cirq

def noisy_bell():
    q0, q1 = cirq.LineQubit.range(2)
    bell = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='meas')
    )
    noisy_bell_circ = bell.with_noise(cirq.depolarize(p=0.01))
    simulator = cirq.Simulator()
    result = simulator.run(noisy_bell_circ, repetitions=1000)
    samples = result.measurements['meas']
    counts = {}
    for sample in samples:
        bitstring = ''.join(map(str, sample))
        counts[bitstring] = counts.get(bitstring, 0) + 1
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
