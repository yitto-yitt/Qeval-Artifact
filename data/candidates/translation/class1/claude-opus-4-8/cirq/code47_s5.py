# EVAL_META: task_id=47, framework=cirq, class=1
import cirq

def random_coin_flip(samples):
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q))
    circuit.append(cirq.measure(q, key='m'))
    result = cirq.Simulator().run(circuit, repetitions=samples)
    counts = result.histogram(key='m')
    total = sum(counts.values())
    return {'Heads': counts.get(0, 0) / total, 'Tails': counts.get(1, 0) / total}
