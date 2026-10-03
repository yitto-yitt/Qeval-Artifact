# EVAL_META: task_id=54, framework=cirq, class=1
import cirq
def and_gate(a, b):
    qa = [cirq.LineQubit(i) for i in range(3)]
    qb = [cirq.LineQubit(i + 3) for i in range(3)]
    qanc = [cirq.LineQubit(i + 6) for i in range(3)]
    circuit = cirq.Circuit()
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    for i in range(3):
        if a_bin[2 - i] == '1':
            circuit.append(cirq.X(qa[i]))
        if b_bin[2 - i] == '1':
            circuit.append(cirq.X(qb[i]))
    for i in range(3):
        circuit.append(cirq.CCX(qa[i], qb[i], qanc[i]))
    circuit.append(cirq.measure(qanc[2], qanc[1], qanc[0], key='measure'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    counts = result.histogram(key='measure')
    total = sum(counts.values())
    return {format(key, '03b'): value / total for key, value in counts.items()}
