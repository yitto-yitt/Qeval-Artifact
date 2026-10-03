# EVAL_META: task_id=56, framework=cirq, class=1
import cirq

def not_gate(a):
    qubits = [cirq.NamedQubit(f'q{i}') for i in range(8)]
    circuit = cirq.Circuit()
    binary = format(a, '08b')
    for i in range(8):
        if binary[7 - i] == '0':
            circuit.append(cirq.X(qubits[i]))
    circuit.append(cirq.measure(*reversed(qubits), key='m'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    counts = {}
    for shot in result.measurements['m']:
        key = ''.join(str(int(b)) for b in shot)
        counts[key] = counts.get(key, 0) + 1
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
