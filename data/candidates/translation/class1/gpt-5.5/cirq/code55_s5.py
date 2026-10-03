# EVAL_META: task_id=55, framework=cirq, class=1
import cirq


def or_gate(a, b):
    qr_a = cirq.LineQubit.range(0, 3)
    qr_b = cirq.LineQubit.range(3, 6)
    ancillary = cirq.LineQubit.range(6, 9)

    circuit = cirq.Circuit()
    a = format(a, "03b")
    b = format(b, "03b")

    for i in range(3):
        if a[2 - i] == "0":
            circuit.append(cirq.X(qr_a[i]))
        if b[2 - i] == "0":
            circuit.append(cirq.X(qr_b[i]))

    for i in range(3):
        circuit.append(cirq.CCX(qr_a[i], qr_b[i], ancillary[i]))

    for q in ancillary:
        circuit.append(cirq.X(q))

    circuit.append(cirq.measure(*ancillary, key="measure"))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)

    counts = {}
    measurements = result.measurements["measure"]
    for row in measurements:
        key = "".join(str(int(bit)) for bit in row[::-1])
        counts[key] = counts.get(key, 0) + 1

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
