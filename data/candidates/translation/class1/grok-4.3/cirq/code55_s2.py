# EVAL_META: task_id=55, framework=cirq, class=1
import cirq

def or_gate(a, b):
    qr_a = [cirq.NamedQubit(f"qr_a_{i}") for i in range(3)]
    qr_b = [cirq.NamedQubit(f"qr_b_{i}") for i in range(3)]
    ancillary = [cirq.NamedQubit(f"ancillary_{i}") for i in range(3)]
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    circuit = cirq.Circuit()
    for i in range(3):
        if a_bin[2 - i] == '0':
            circuit.append(cirq.X(qr_a[i]))
        if b_bin[2 - i] == '0':
            circuit.append(cirq.X(qr_b[i]))
    for i in range(3):
        circuit.append(cirq.CCX(qr_a[i], qr_b[i], ancillary[i]))
    circuit.append([cirq.X(q) for q in ancillary])
    circuit.append(cirq.measure(ancillary[2], ancillary[1], ancillary[0], key='measure'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    counts = result.histogram(key='measure')
    total = sum(counts.values())
    return {format(k, '03b'): v / total for k, v in counts.items()}
