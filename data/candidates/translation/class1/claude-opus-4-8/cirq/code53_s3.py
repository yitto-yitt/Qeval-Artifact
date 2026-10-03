# EVAL_META: task_id=53, framework=cirq, class=1
import cirq

def xor_gate(a, b):
    n = 8
    qubits = [cirq.LineQubit(i) for i in range(n)]
    circuit = cirq.Circuit()
    for i in range(n):
        if (a >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
    for i in range(n):
        if (b >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
    circuit.append(cirq.measure(*qubits, key='meas'))
    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions=1024)
    measurements = result.measurements['meas']
    counts = {}
    for row in measurements:
        key = ''.join(str(int(bit)) for bit in row[::-1])
        counts[key] = counts.get(key, 0) + 1
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
