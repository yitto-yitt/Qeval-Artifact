# EVAL_META: task_id=54, framework=cirq, class=1
import cirq

def and_gate(a, b):
    q_a = [cirq.NamedQubit(f'a{i}') for i in range(3)]
    q_b = [cirq.NamedQubit(f'b{i}') for i in range(3)]
    anc = [cirq.NamedQubit(f'anc{i}') for i in range(3)]

    circuit = cirq.Circuit()

    a_str = format(a, '03b')
    b_str = format(b, '03b')

    for i in range(3):
        if a_str[2 - i] == '1':
            circuit.append(cirq.X(q_a[i]))
        if b_str[2 - i] == '1':
            circuit.append(cirq.X(q_b[i]))

    for i in range(3):
        circuit.append(cirq.TOFFOLI(q_a[i], q_b[i], anc[i]))

    circuit.append(cirq.measure(anc[2], anc[1], anc[0], key='result'))

    simulator = cirq.Simulator()
    results = simulator.run(circuit, repetitions=1000)

    bitstrings = results.measurements['result']
    counts = {}
    for row in bitstrings:
        bitstring = ''.join(str(int(bit)) for bit in row)
        counts[bitstring] = counts.get(bitstring, 0) + 1

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
