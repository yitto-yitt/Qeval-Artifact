# EVAL_META: task_id=54, framework=cirq, class=1
import cirq

def and_gate(a, b):
    qr_a = [cirq.NamedQubit(f'qr_a_{i}') for i in range(3)]
    qr_b = [cirq.NamedQubit(f'qr_b_{i}') for i in range(3)]
    ancillary = [cirq.NamedQubit(f'ancillary_{i}') for i in range(3)]
    measure = [cirq.NamedQubit(f'measure_{i}') for i in range(3)]

    a_bits = format(a, '03b')
    b_bits = format(b, '03b')

    circuit = cirq.Circuit()

    for i in range(3):
        if a_bits[2 - i] == '1':
            circuit.append(cirq.X(qr_a[i]))
        if b_bits[2 - i] == '1':
            circuit.append(cirq.X(qr_b[i]))

    for i in range(3):
        circuit.append(cirq.CCX(qr_a[i], qr_b[i], ancillary[i]))

    circuit.append(cirq.measure(*ancillary, key='result'))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    counts = result.histogram(key='result')

    total = sum(counts.values())
    return {format(k, '03b'): v / total for k, v in counts.items()}
