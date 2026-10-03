# EVAL_META: task_id=54, framework=cirq, class=1
import cirq


def and_gate(a, b):
    qr_a = [cirq.NamedQubit(f"qr_a_{i}") for i in range(3)]
    qr_b = [cirq.NamedQubit(f"qr_b_{i}") for i in range(3)]
    ancillary = [cirq.NamedQubit(f"ancillary_{i}") for i in range(3)]

    circuit = cirq.Circuit()
    a_bits = format(a, "03b")
    b_bits = format(b, "03b")

    for i in range(3):
        if a_bits[2 - i] == "1":
            circuit.append(cirq.X(qr_a[i]))
        if b_bits[2 - i] == "1":
            circuit.append(cirq.X(qr_b[i]))

    for i in range(3):
        circuit.append(cirq.CCX(qr_a[i], qr_b[i], ancillary[i]))

    circuit.append(cirq.measure(*ancillary, key="measure"))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    histogram = result.multi_measurement_histogram(keys=["measure"])

    total = sum(histogram.values())
    distribution = {}
    for key, count in histogram.items():
        bits = key[0]
        bitstring = "".join(str(bit) for bit in bits[::-1])
        distribution[bitstring] = count / total

    return distribution
