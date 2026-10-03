# EVAL_META: task_id=54, framework=cirq, class=1
import cirq

def and_gate(a, b):
    qr_a = [cirq.LineQubit(i) for i in range(3)]
    qr_b = [cirq.LineQubit(3 + i) for i in range(3)]
    anc = [cirq.LineQubit(6 + i) for i in range(3)]
    a = format(a, '03b')
    b = format(b, '03b')
    circuit = cirq.Circuit()
    for i in range(3):
        if a[2 - i] == '1':
            circuit.append(cirq.X(qr_a[i]))
        if b[2 - i] == '1':
            circuit.append(cirq.X(qr_b[i]))
    for i in range(3):
        circuit.append(cirq.CCX(qr_a[i], qr_b[i], anc[i]))
    circuit.append(cirq.measure(*anc, key='measure'))
    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions=1024)
    hist = result.multi_measurement_histogram(keys=['measure'])
    counts = {}
    total = 0
    for key, value in hist.items():
        bits = key[0]
        s = ''.join(str(bits[2 - i]) for i in range(3))
        counts[s] = counts.get(s, 0) + value
        total += value
    return {k: v / total for k, v in counts.items()}
