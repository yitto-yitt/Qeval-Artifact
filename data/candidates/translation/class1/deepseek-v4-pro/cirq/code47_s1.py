# EVAL_META: task_id=47, framework=cirq, class=1
import cirq
import numpy as np

def random_coin_flip(samples):
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit([cirq.H(q), cirq.measure(q, key='result')])
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=samples)
    measurements = result.measurements['result']
    counts = np.bincount(measurements.flatten(), minlength=2)
    total = counts.sum()
    return {'Heads': counts[0] / total, 'Tails': counts[1] / total}
