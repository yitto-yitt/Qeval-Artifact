# EVAL_META: task_id=54, framework=cirq, class=1
import cirq
import numpy as np

def and_gate(a, b):
    qr_a = [cirq.LineQubit(i) for i in range(3)]
    qr_b = [cirq.LineQubit(i + 3) for i in range(3)]
    ancillary = [cirq.LineQubit(i + 6) for i in range(3)]
    measure = [cirq.LineQubit(i + 9) for i in range(3)]

    a_bin = format(a, '03b')
    b_bin = format(b, '03b')

    circuit = cirq.Circuit()

    for i in range(3):
        if a_bin[2 - i] == '1':
            circuit.append(cirq.X(qr_a[i]))
        if b_bin[2 - i] == '1':
            circuit.append(cirq.X(qr_b[i]))

    for i in range(3):
        circuit.append(cirq.CCX(qr_a[i], qr_b[i], ancillary[i]))

    circuit.append(cirq.measure(*ancillary, key='result'))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10000)
    counts = result.histogram(key='result')

    total = sum(counts.values())
    prob_dist = {}
    for outcome, count in counts.items():
        prob_dist[format(outcome, '03b')] = count / total

    return prob_dist
