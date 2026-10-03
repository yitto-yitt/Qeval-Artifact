# EVAL_META: task_id=55, framework=cirq, class=1
import cirq

def or_gate(a, b):
    qa = [cirq.NamedQubit(f"qa_{i}") for i in range(3)]
    qb = [cirq.NamedQubit(f"qb_{i}") for i in range(3)]
    anc = [cirq.NamedQubit(f"anc_{i}") for i in range(3)]
    circuit = cirq.Circuit()
    a_bin = format(a, "03b")
    b_bin = format(b, "03b")
    for i in range(3):
        if a_bin[2 - i] == "0":
            circuit.append(cirq.X(qa[i]))
        if b_bin[2 - i] == "0":
            circuit.append(cirq.X(qb[i]))
    for i in range(3):
        circuit.append(cirq.CCX(qa[i], qb[i], anc[i]))
    circuit.append(cirq.X.on_each(anc))
    circuit.append(cirq.measure(anc[2], anc[1], anc[0], key="m"))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    counts = result.histogram(key="m")
    total = sum(counts.values())
    return {format(bits_int, "03b"): count / total for bits_int, count in counts.items()}
