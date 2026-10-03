# EVAL_META: task_id=53, framework=cirq, class=1
import cirq

def xor_gate(a, b):
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()

    # Apply XOR with a
    for i in range(8):
        if (a >> i) & 1:
            circuit.append(cirq.X(qubits[i]))

    # Apply XOR with b
    for i in range(8):
        if (b >> i) & 1:
            circuit.append(cirq.X(qubits[i]))

    circuit.append(cirq.measure(*qubits, key='result'))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    counts = result.histogram(key='result')

    # Convert counts to 8-bit binary strings
    total = sum(counts.values())
    prob_dist = {}
    for state, count in counts.items():
        bitstring = format(state, '08b')
        prob_dist[bitstring] = count / total

    return prob_dist
