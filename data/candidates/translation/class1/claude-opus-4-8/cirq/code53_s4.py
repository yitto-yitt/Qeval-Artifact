# EVAL_META: task_id=53, framework=cirq, class=1
import cirq

def xor_gate(a, b):
    n = 8
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    # XOR with constant a, then XOR with constant b, starting from |0>
    for val in (a, b):
        for i in range(n):
            if (val >> i) & 1:
                # bit i corresponds to qubit index (n-1-i) so that
                # measurement string reads as standard binary
                circuit.append(cirq.X(qubits[n - 1 - i]))
    circuit.append(cirq.measure(*qubits, key='meas'))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    measurements = result.measurements['meas']

    counts = {}
    for row in measurements:
        key = ''.join(str(int(bit)) for bit in row)
        counts[key] = counts.get(key, 0) + 1

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
