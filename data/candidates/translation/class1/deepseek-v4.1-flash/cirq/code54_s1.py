# EVAL_META: task_id=54, framework=cirq, class=1
import cirq

def and_gate(a, b):
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    qubits = cirq.LineQubit.range(9)
    qr_a = qubits[0:3]
    qr_b = qubits[3:6]
    ancillary = qubits[6:9]
    circuit = cirq.Circuit()
    for i in range(3):
        if a_bin[2-i] == '1':
            circuit.append(cirq.X(qr_a[i]))
        if b_bin[2-i] == '1':
            circuit.append(cirq.X(qr_b[i]))
    for i in range(3):
        circuit.append(cirq.TOFFOLI(qr_a[i], qr_b[i], ancillary[i]))
    circuit.append(cirq.measure(ancillary[2], ancillary[1], ancillary[0], key='m'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    counts = result.histogram(key='m')
    total = sum(counts.values())
    return {format(k, '03b'): v / total for k, v in counts.items()}
