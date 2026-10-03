# EVAL_META: task_id=55, framework=cirq, class=1
import cirq

def or_gate(a, b):
    qubits_a = cirq.LineQubit.range(3)
    qubits_b = cirq.LineQubit.range(3, 6)
    ancillary = cirq.LineQubit.range(6, 9)
    circuit = cirq.Circuit()

    a_str = format(a, '03b')
    b_str = format(b, '03b')

    for i in range(3):
        if a_str[2 - i] == '0':
            circuit.append(cirq.X(qubits_a[i]))
        if b_str[2 - i] == '0':
            circuit.append(cirq.X(qubits_b[i]))

    for i in range(3):
        circuit.append(cirq.CCX(qubits_a[i], qubits_b[i], ancillary[i]))

    circuit.append(cirq.X.on_each(*ancillary))
    circuit.append(cirq.measure(*ancillary, key='result'))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10000)
    counts = result.histogram(key='result')

    total = sum(counts.values())
    distribution = {}
    for outcome in range(8):
        bitstring = format(outcome, '03b')
        count = counts.get(outcome, 0)
        distribution[bitstring] = count / total

    return distribution
