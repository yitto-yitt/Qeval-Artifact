# EVAL_META: task_id=54, framework=cirq, class=1
import cirq

def and_gate(a, b):
    qr_a = cirq.LineQubit.range(3)
    qr_b = cirq.LineQubit.range(3, 6)
    ancillary = cirq.LineQubit.range(6, 9)
    circuit = cirq.Circuit()
    a = format(a, '03b')
    b = format(b, '03b')
    for i in range(3):
        if a[2 - i] == '1':
            circuit.append(cirq.X(qr_a[i]))
        if b[2 - i] == '1':
            circuit.append(cirq.X(qr_b[i]))
    for i in range(3):
        circuit.append(cirq.CCX(qr_a[i], qr_b[i], ancillary[i]))
    circuit.append(cirq.measure(*reversed(ancillary), key="measure"))
    result = cirq.Simulator().run(circuit, repetitions=1024)
    counts = result.histogram(key="measure")
    total = sum(counts.values())
    return {format(key, '03b'): value / total for key, value in counts.items()}
