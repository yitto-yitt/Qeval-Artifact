# EVAL_META: task_id=47, framework=cirq, class=1
import cirq

def random_coin_flip(samples):
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit(cirq.H(q), cirq.measure(q, key='m'))
    result = cirq.Simulator().run(circuit, repetitions=samples)
    bits = result.measurements['m'].reshape(-1)
    total = len(bits)
    tails = int(bits.sum())
    heads = total - tails
    return {'Heads': heads / total, 'Tails': tails / total}
