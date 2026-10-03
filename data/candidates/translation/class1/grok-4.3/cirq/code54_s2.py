# EVAL_META: task_id=54, framework=cirq, class=1
import cirq
from collections import Counter

def and_gate(a, b):
    qubits_a = [cirq.LineQubit(i) for i in range(3)]
    qubits_b = [cirq.LineQubit(i + 3) for i in range(3)]
    qubits_anc = [cirq.LineQubit(i + 6) for i in range(3)]
    circuit = cirq.Circuit()
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    for i in range(3):
        if a_bin[2 - i] == '1':
            circuit.append(cirq.X(qubits_a[i]))
        if b_bin[2 - i] == '1':
            circuit.append(cirq.X(qubits_b[i]))
    for i in range(3):
        circuit.append(cirq.CCX(qubits_a[i], qubits_b[i], qubits_anc[i]))
    circuit.append(cirq.measure(qubits_anc[2], qubits_anc[1], qubits_anc[0], key='result'))
    simulator = cirq.Simulator()
    repetitions = 1024
    result = simulator.run(circuit, repetitions=repetitions)
    counts = Counter()
    for measurement in result.measurements['result']:
        bin_str = ''.join(str(bit) for bit in measurement)
        counts[bin_str] += 1
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
