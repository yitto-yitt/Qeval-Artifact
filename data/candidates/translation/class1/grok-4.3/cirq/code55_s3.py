# EVAL_META: task_id=55, framework=cirq, class=1
import cirq
from collections import Counter

def or_gate(a, b):
    qr_a = [cirq.LineQubit(i) for i in range(3)]
    qr_b = [cirq.LineQubit(i + 3) for i in range(3)]
    ancillary = [cirq.LineQubit(i + 6) for i in range(3)]
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    circuit = cirq.Circuit()
    for i in range(3):
        if a_str[2 - i] == '0':
            circuit.append(cirq.X(qr_a[i]))
        if b_str[2 - i] == '0':
            circuit.append(cirq.X(qr_b[i]))
    for i in range(3):
        circuit.append(cirq.CCX(qr_a[i], qr_b[i], ancillary[i]))
    circuit.append([cirq.X(q) for q in ancillary])
    measure_qubits = [ancillary[2], ancillary[1], ancillary[0]]
    circuit.append(cirq.measure(*measure_qubits, key='result'))
    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions=1024)
    samples = result.measurements['result']
    count_dict = Counter(''.join(map(str, s)) for s in samples)
    total = sum(count_dict.values())
    return {k: v / total for k, v in count_dict.items()}
