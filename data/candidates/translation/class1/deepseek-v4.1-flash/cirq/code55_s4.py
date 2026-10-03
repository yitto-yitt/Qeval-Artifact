# EVAL_META: task_id=55, framework=cirq, class=1
import cirq

def or_gate(a, b):
    a_bits = format(a, '03b')
    b_bits = format(b, '03b')
    qa = [cirq.NamedQubit(f'a{i}') for i in range(3)]
    qb = [cirq.NamedQubit(f'b{i}') for i in range(3)]
    qanc = [cirq.NamedQubit(f'anc{i}') for i in range(3)]
    circuit = cirq.Circuit()
    for i in range(3):
        if a_bits[2-i] == '0':
            circuit.append(cirq.X(qa[i]))
        if b_bits[2-i] == '0':
            circuit.append(cirq.X(qb[i]))
    for i in range(3):
        circuit.append(cirq.TOFFOLI(qa[i], qb[i], qanc[i]))
    for i in range(3):
        circuit.append(cirq.X(qanc[i]))
    circuit.append(cirq.measure(*qanc[::-1], key='m'))
    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions=1000)
    counts = result.histogram(key='m')
    total = sum(counts.values())
    return {format(k, '03b'): v / total for k, v in counts.items()}
