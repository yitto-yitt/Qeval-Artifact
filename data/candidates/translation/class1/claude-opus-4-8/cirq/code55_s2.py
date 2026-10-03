# EVAL_META: task_id=55, framework=cirq, class=1
import cirq

def or_gate(a, b):
    qr_a = [cirq.LineQubit(i) for i in range(3)]
    qr_b = [cirq.LineQubit(i + 3) for i in range(3)]
    ancillary = [cirq.LineQubit(i + 6) for i in range(3)]
    circuit = cirq.Circuit()
    a = format(a, '03b')
    b = format(b, '03b')
    for i in range(3):
        if a[2 - i] == '0':
            circuit.append(cirq.X(qr_a[i]))
        if b[2 - i] == '0':
            circuit.append(cirq.X(qr_b[i]))
    for i in range(3):
        circuit.append(cirq.CCX(qr_a[i], qr_b[i], ancillary[i]))
    for i in range(3):
        circuit.append(cirq.X(ancillary[i]))
    circuit.append(cirq.measure(*ancillary, key='measure'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    hist = result.histogram(key='measure')
    total = sum(hist.values())
    return {format(key, '03b'): value / total for key, value in hist.items()}
