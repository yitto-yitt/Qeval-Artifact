# EVAL_META: task_id=54, framework=cirq, class=1
import cirq
import collections

def and_gate(a, b):
    a_qubits = [cirq.NamedQubit(f'a{i}') for i in range(3)]
    b_qubits = [cirq.NamedQubit(f'b{i}') for i in range(3)]
    anc_qubits = [cirq.NamedQubit(f'anc{i}') for i in range(3)]
    circuit = cirq.Circuit()
    for i in range(3):
        if (a >> i) & 1:
            circuit.append(cirq.X(a_qubits[i]))
        if (b >> i) & 1:
            circuit.append(cirq.X(b_qubits[i]))
    for i in range(3):
        circuit.append(cirq.TOFFOLI(a_qubits[i], b_qubits[i], anc_qubits[i]))
    circuit.append(cirq.measure(anc_qubits[2], anc_qubits[1], anc_qubits[0], key='m'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    counts = collections.Counter()
    for outcome in result.measurements['m']:
        bitstring = ''.join(str(int(bit)) for bit in outcome)
        counts[bitstring] += 1
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
