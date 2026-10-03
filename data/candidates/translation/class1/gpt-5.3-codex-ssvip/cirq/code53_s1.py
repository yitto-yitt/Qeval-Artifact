# EVAL_META: task_id=53, framework=cirq, class=1
import cirq


def xor_gate(a, b):
    qubits = [cirq.LineQubit(i) for i in range(8)]
    circuit = cirq.Circuit()

    x = a ^ b
    for i in range(8):
        if (x >> i) & 1:
            circuit.append(cirq.X(qubits[i]))

    circuit.append(cirq.measure(*qubits, key='meas'))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    counts = result.multi_measurement_histogram(keys=['meas'])

    total = sum(counts.values())
    distribution = {}
    for (bits,), count in counts.items():
        bitstring = ''.join(str(bit) for bit in bits[::-1])
        distribution[bitstring] = count / total

    return distribution
