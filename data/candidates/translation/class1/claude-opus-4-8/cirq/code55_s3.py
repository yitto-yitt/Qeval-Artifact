# EVAL_META: task_id=55, framework=cirq, class=1
import cirq

def or_gate(a, b):
    qr_a = [cirq.LineQubit(i) for i in range(3)]
    qr_b = [cirq.LineQubit(3 + i) for i in range(3)]
    anc = [cirq.LineQubit(6 + i) for i in range(3)]
    circuit = cirq.Circuit()
    a = format(a, '03b')
    b = format(b, '03b')
    for i in range(3):
        if a[2 - i] == '0':
            circuit.append(cirq.X(qr_a[i]))
        if b[2 - i] == '0':
            circuit.append(cirq.X(qr_b[i]))
    for i in range(3):
        circuit.append(cirq.TOFFOLI(qr_a[i], qr_b[i], anc[i]))
    for i in range(3):
        circuit.append(cirq.X(anc[i]))
    circuit.append(cirq.measure(*anc, key='measure'))

    sim = cirq.Simulator()
    reps = 1024
    result = sim.run(circuit, repetitions=reps)
    data = result.measurements['measure']  # shape (reps, 3), columns anc0,anc1,anc2

    counts = {}
    for shot in data:
        key = f"{shot[2]}{shot[1]}{shot[0]}"
        counts[key] = counts.get(key, 0) + 1
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
