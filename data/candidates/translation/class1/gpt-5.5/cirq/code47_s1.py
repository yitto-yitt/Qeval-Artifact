# EVAL_META: task_id=47, framework=cirq, class=1
import cirq


def random_coin_flip(samples):
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit(
        cirq.H(qubit),
        cirq.measure(qubit, key='meas')
    )
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=samples)
    measurements = result.measurements['meas'][:, 0]
    heads = int((measurements == 0).sum())
    tails = int((measurements == 1).sum())
    total = heads + tails
    return {'Heads': heads / total, 'Tails': tails / total}
