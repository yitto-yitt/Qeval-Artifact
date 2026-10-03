# EVAL_META: task_id=55, framework=cirq, class=1
import cirq
from collections import Counter

def or_gate(a, b):
    a_bits = format(a, '03b')
    b_bits = format(b, '03b')
    qr_a = [cirq.LineQubit(i) for i in range(3)]
    qr_b = [cirq.LineQubit(i + 3) for i in range(3)]
    anc = [cirq.LineQubit(i + 6) for i in range(3)]
    circuit = cirq.Circuit()
    for i in range(3):
        if a_bits[2 - i] == '0':
            circuit.append(cirq.X(qr_a[i]))
        if b_bits[2 - i] == '0':
            circuit.append(cirq.X(qr_b[i]))
    for i in range(3):
        circuit.append(cirq.TOFFOLI(qr_a[i], qr_b[i], anc[i]))
    for i in range(3):
        circuit.append(cirq.X(anc[i]))
    circuit.append(cirq.measure(anc[2], anc[1], anc[0], key='m'))
    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions=1024)
    counts = Counter()
    for bits in result.measurements['m']:
        key = ''.join(str(int(b)) for b in bits)
        counts[key] += 1
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
