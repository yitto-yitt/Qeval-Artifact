# EVAL_META: task_id=55, framework=cirq, class=1
import cirq


def or_gate(a, b):
    qa = [cirq.LineQubit(i) for i in range(3)]
    qb = [cirq.LineQubit(i + 3) for i in range(3)]
    anc = [cirq.LineQubit(i + 6) for i in range(3)]

    circuit = cirq.Circuit()

    a_bits = format(a, "03b")
    b_bits = format(b, "03b")

    for i in range(3):
        if a_bits[2 - i] == "0":
            circuit.append(cirq.X(qa[i]))
        if b_bits[2 - i] == "0":
            circuit.append(cirq.X(qb[i]))

    for i in range(3):
        circuit.append(cirq.TOFFOLI(qa[i], qb[i], anc[i]))

    for i in range(3):
        circuit.append(cirq.X(anc[i]))

    circuit.append(cirq.measure(*anc, key="measure"))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    hist = result.multi_measurement_histogram(keys=["measure"])
    counts = {}
    for key_tuple, count in hist.items():
        bits = key_tuple[0]
        bitstring = "".join(str(bit) for bit in bits[::-1])
        counts[bitstring] = counts.get(bitstring, 0) + count

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
