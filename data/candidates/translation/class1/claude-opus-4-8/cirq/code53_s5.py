# EVAL_META: task_id=53, framework=cirq, class=1
import cirq

def xor_gate(a, b):
    n = 8
    value = a ^ b
    qubits = [cirq.LineQubit(i) for i in range(n)]
    circuit = cirq.Circuit()
    for i in range(n):
        if (a >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
    for i in range(n):
        if (b >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
    circuit.append(cirq.measure(*qubits, key='meas'))

    simulator = cirq.Simulator()
    shots = 1024
    result = simulator.run(circuit, repetitions=shots)
    measurements = result.measurements['meas']

    counts = {}
    for row in measurements:
        # row[i] corresponds to qubit i (bit i). Build MSB-first string.
        key = ''.join(str(int(row[i])) for i in range(n - 1, -1, -1))
        counts[key] = counts.get(key, 0) + 1

    total = sum(counts.values())
    return {key: val / total for key, val in counts.items()}
