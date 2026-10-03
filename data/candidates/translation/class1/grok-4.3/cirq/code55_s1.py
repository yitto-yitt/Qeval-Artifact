# EVAL_META: task_id=55, framework=cirq, class=1
import cirq

def or_gate(a, b):
    qa = [cirq.NamedQubit(f"a{i}") for i in range(3)]
    qb = [cirq.NamedQubit(f"b{i}") for i in range(3)]
    qanc = [cirq.NamedQubit(f"anc{i}") for i in range(3)]
    circuit = cirq.Circuit()
    a_str = format(a, "03b")
    b_str = format(b, "03b")
    for i in range(3):
        if a_str[2 - i] == "0":
            circuit.append(cirq.X(qa[i]))
        if b_str[2 - i] == "0":
            circuit.append(cirq.X(qb[i]))
    for i in range(3):
        circuit.append(cirq.CCX(qa[i], qb[i], qanc[i]))
    for i in range(3):
        circuit.append(cirq.X(qanc[i]))
    circuit.append(cirq.measure(*qanc, key="m"))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    counts = result.histogram(key="m")
    total = sum(counts.values())
    return {format(k, "03b"): v / total for k, v in counts.items()}
