# EVAL_META: task_id=54, framework=cirq, class=1
import cirq

def and_gate(a, b):
    qr_a = [cirq.NamedQubit(f"qr_a_{i}") for i in range(3)]
    qr_b = [cirq.NamedQubit(f"qr_b_{i}") for i in range(3)]
    ancillary = [cirq.NamedQubit(f"ancillary_{i}") for i in range(3)]
    circuit = cirq.Circuit()
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    for i in range(3):
        if a_bin[2 - i] == '1':
            circuit.append(cirq.X(qr_a[i]))
        if b_bin[2 - i] == '1':
            circuit.append(cirq.X(qr_b[i]))
    for i in range(3):
        circuit.append(cirq.CCNOT(qr_a[i], qr_b[i], ancillary[i]))
    circuit.append(cirq.measure(*ancillary, key='measure'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    measurements = result.measurements['measure']
    counts = {}
    for shot in measurements:
        bin_str = ''.join(str(bit) for bit in shot[::-1])
        counts[bin_str] = counts.get(bin_str, 0) + 1
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
