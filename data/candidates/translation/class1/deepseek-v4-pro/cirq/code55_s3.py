# EVAL_META: task_id=55, framework=cirq, class=1
import cirq
import numpy as np

def or_gate(a, b):
    # Qubit registers
    qr_a = [cirq.LineQubit(i) for i in range(3)]
    qr_b = [cirq.LineQubit(i + 3) for i in range(3)]
    ancillary = [cirq.LineQubit(i + 6) for i in range(3)]
    measure = [cirq.LineQubit(i + 9) for i in range(3)]

    # Build circuit
    circuit = cirq.Circuit()

    # Encode inputs (bitwise NOT because we want OR via De Morgan: a OR b = NOT(NOT a AND NOT b))
    a_bits = format(a, '03b')
    b_bits = format(b, '03b')
    for i in range(3):
        if a_bits[2 - i] == '0':
            circuit.append(cirq.X(qr_a[i]))
        if b_bits[2 - i] == '0':
            circuit.append(cirq.X(qr_b[i]))

    # Compute AND of inverted inputs
    for i in range(3):
        circuit.append(cirq.CCX(qr_a[i], qr_b[i], ancillary[i]))

    # Invert to get OR
    circuit.append(cirq.X.on_each(*ancillary))

    # Measure
    circuit.append(cirq.measure(*ancillary, key='result'))

    # Simulate
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10000)
    hist = result.histogram(key='result')

    # Convert to probability distribution with 3-bit strings
    total = sum(hist.values())
    prob_dist = {}
    for outcome, count in hist.items():
        bitstring = format(outcome, '03b')
        prob_dist[bitstring] = count / total

    return prob_dist
