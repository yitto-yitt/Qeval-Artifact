# EVAL_META: task_id=55, framework=cirq, class=1
import cirq


def or_gate(a, b):
    qr_a = [cirq.NamedQubit(f"qr_a_{i}") for i in range(3)]
    qr_b = [cirq.NamedQubit(f"qr_b_{i}") for i in range(3)]
    ancillary = [cirq.NamedQubit(f"ancillary_{i}") for i in range(3)]

    circuit = cirq.Circuit()
    a_bits = format(a, "03b")
    b_bits = format(b, "03b")

    for i in range(3):
        if a_bits[2 - i] == "0":
            circuit.append(cirq.X(qr_a[i]))
        if b_bits[2 - i] == "0":
            circuit.append(cirq.X(qr_b[i]))

    for i in range(3):
        circuit.append(cirq.TOFFOLI(qr_a[i], qr_b[i], ancillary[i]))

    for q in ancillary:
        circuit.append(cirq.X(q))

    circuit.append(cirq.measure(*ancillary, key="measure"))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    histogram = result.multi_measurement_histogram(keys=["measure"])

    counts = {}
    for key_tuple, count in histogram.items():
        bits = key_tuple[0]
        bitstring = "".join(str(bit) for bit in bits[::-1])
        counts[bitstring] = counts.get(bitstring, 0) + count

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
