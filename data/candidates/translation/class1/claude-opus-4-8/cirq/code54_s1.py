# EVAL_META: task_id=54, framework=cirq, class=1
import cirq

def and_gate(a, b):
    qr_a = [cirq.NamedQubit(f"qr_a_{i}") for i in range(3)]
    qr_b = [cirq.NamedQubit(f"qr_b_{i}") for i in range(3)]
    ancillary = [cirq.NamedQubit(f"ancillary_{i}") for i in range(3)]
    a = format(a, '03b')
    b = format(b, '03b')
    circuit = cirq.Circuit()
    for i in range(3):
        if a[2-i] == '1':
            circuit.append(cirq.X(qr_a[i]))
        if b[2-i] == '1':
            circuit.append(cirq.X(qr_b[i]))
    for i in range(3):
        circuit.append(cirq.CCX(qr_a[i], qr_b[i], ancillary[i]))
    circuit.append(cirq.measure(*ancillary, key="measure"))
    simulator = cirq.Simulator()
    reps = 1024
    result = simulator.run(circuit, repetitions=reps)
    measurements = result.measurements["measure"]
    counts = {}
    for row in measurements:
        key = "".join(str(int(b)) for b in row)
        counts[key] = counts.get(key, 0) + 1
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
