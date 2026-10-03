# EVAL_META: task_id=47, framework=cirq, class=1
import cirq

def random_coin_flip(samples):
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit(cirq.H(qubit), cirq.measure(qubit, key='m'))
    result = cirq.Simulator().run(circuit, repetitions=samples)
    measurements = result.measurements['m']
    counts = {0: 0, 1: 0}
    for bit in measurements.reshape(-1):
        counts[int(bit)] += 1
    total = sum(counts.values())
    return {'Heads': counts[0] / total, 'Tails': counts[1] / total}
