# EVAL_META: task_id=47, framework=cirq, class=1
import cirq

def random_coin_flip(samples):
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit(cirq.H(qubit), cirq.measure(qubit, key='m'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=samples)
    histogram = result.histogram(key='m')
    total = sum(histogram.values())
    return {
        'Heads': histogram.get(0, 0) / total,
        'Tails': histogram.get(1, 0) / total,
    }
