# EVAL_META: task_id=47, framework=cirq, class=1
import cirq

def random_coin_flip(samples):
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit(
        cirq.H(qubit),
        cirq.measure(qubit, key="meas"),
    )
    result = cirq.Simulator().run(circuit, repetitions=samples)
    counts = result.histogram(key="meas")
    total = sum(counts.values())
    return {
        'Heads': counts.get(0, 0) / total,
        'Tails': counts.get(1, 0) / total,
    }
