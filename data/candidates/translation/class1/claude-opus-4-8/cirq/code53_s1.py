# EVAL_META: task_id=53, framework=cirq, class=1
import cirq

def xor_gate(a, b):
    qubits = [cirq.LineQubit(i) for i in range(8)]
    circuit = cirq.Circuit()
    for i in range(8):
        if (a >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
    for i in range(8):
        if (b >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
    circuit.append(cirq.measure(*qubits, key='meas'))
    simulator = cirq.Simulator()
    reps = 1024
    result = simulator.run(circuit, repetitions=reps)
    measurements = result.measurements['meas']
    counts = {}
    for shot in measurements:
        key = ''.join(str(int(bit)) for bit in shot[::-1])
        counts[key] = counts.get(key, 0) + 1
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
