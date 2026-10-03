# EVAL_META: task_id=54, framework=cirq, class=1
import cirq

def and_gate(a, b):
    qr_a = [cirq.LineQubit(i) for i in range(3)]
    qr_b = [cirq.LineQubit(3 + i) for i in range(3)]
    anc = [cirq.LineQubit(6 + i) for i in range(3)]
    circuit = cirq.Circuit()
    a = format(a, '03b')
    b = format(b, '03b')
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
    meas = result.measurements['measure']
    counts = {}
    for row in meas:
        key = ''.join(str(int(x)) for x in row[::-1])
        counts[key] = counts.get(key, 0) + 1
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
