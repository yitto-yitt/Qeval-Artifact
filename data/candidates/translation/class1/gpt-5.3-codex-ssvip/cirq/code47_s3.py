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
    heads = int((measurements == 0).sum())
    tails = int((measurements == 1).sum())
    total = heads + tails
    return {
        'Heads': heads / total if total else 0.0,
        'Tails': tails / total if total else 0.0
    }
