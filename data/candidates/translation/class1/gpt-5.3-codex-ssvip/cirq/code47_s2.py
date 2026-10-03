# EVAL_META: task_id=47, framework=cirq, class=1
import cirq

def random_coin_flip(samples):
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit(
        cirq.H(q),
        cirq.measure(q, key='meas')
    )
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=samples)
    measurements = result.measurements['meas'].flatten()
    heads_count = int((measurements == 0).sum())
    tails_count = int((measurements == 1).sum())
    total = heads_count + tails_count
    return {
        'Heads': heads_count / total,
        'Tails': tails_count / total
    }
