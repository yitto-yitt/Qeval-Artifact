# EVAL_META: task_id=54, framework=cirq, class=1
import cirq

def and_gate(a, b):
    qa = [cirq.LineQubit(i) for i in range(3)]
    qb = [cirq.LineQubit(i + 3) for i in range(3)]
    qanc = [cirq.LineQubit(i + 6) for i in range(3)]
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    circuit = cirq.Circuit()
    for i in range(3):
        if a_str[2 - i] == '1':
            circuit.append(cirq.X(qa[i]))
        if b_str[2 - i] == '1':
            circuit.append(cirq.X(qb[i]))
    for i in range(3):
        circuit.append(cirq.CCX(qa[i], qb[i], qanc[i]))
    circuit.append(cirq.measure(qanc[2], qanc[1], qanc[0], key='result'))
    sim = cirq.Simulator()
    res = sim.run(circuit, repetitions=1024)
    counts = res.histogram(key='result')
    total = sum(counts.values())
    return {format(k, '03b'): v / total for k, v in counts.items()}
