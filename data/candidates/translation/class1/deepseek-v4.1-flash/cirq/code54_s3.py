# EVAL_META: task_id=54, framework=cirq, class=1
import cirq

def and_gate(a, b):
    qr_a = [cirq.NamedQubit(f'a{i}') for i in range(3)]
    qr_b = [cirq.NamedQubit(f'b{i}') for i in range(3)]
    ancillary = [cirq.NamedQubit(f'anc{i}') for i in range(3)]
    circuit = cirq.Circuit()
    a_bits = format(a, '03b')
    b_bits = format(b, '03b')
    for i in range(3):
        if a_bits[2 - i] == '1':
            circuit.append(cirq.X(qr_a[i]))
        if b_bits[2 - i] == '1':
            circuit.append(cirq.X(qr_b[i]))
    for i in range(3):
        circuit.append(cirq.TOFFOLI(qr_a[i], qr_b[i], ancillary[i]))
    circuit.append(cirq.measure(ancillary[2], ancillary[1], ancillary[0], key='m'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    bits = result.measurements['m']
    counts = {}
    for row in bits:
        key = ''.join(str(int(b)) for b in row)
        counts[key] = counts.get(key, 0) + 1
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
