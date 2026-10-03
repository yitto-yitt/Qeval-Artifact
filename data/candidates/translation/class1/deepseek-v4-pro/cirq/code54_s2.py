# EVAL_META: task_id=54, framework=cirq, class=1
import cirq
import numpy as np

def and_gate(a, b):
    # Convert integers to 3-bit binary strings
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')

    # Define qubits
    qr_a = [cirq.NamedQubit(f'qr_a_{i}') for i in range(3)]
    qr_b = [cirq.NamedQubit(f'qr_b_{i}') for i in range(3)]
    ancillary = [cirq.NamedQubit(f'ancillary_{i}') for i in range(3)]

    # Build circuit
    circuit = cirq.Circuit()

    # Apply X gates for '1' bits (Qiskit uses little-endian: a[2-i] corresponds to qr_a[i])
    for i in range(3):
        if a_bin[2 - i] == '1':
            circuit.append(cirq.X(qr_a[i]))
        if b_bin[2 - i] == '1':
            circuit.append(cirq.X(qr_b[i]))

    # Apply Toffoli (CCX) gates for bitwise AND
    for i in range(3):
        circuit.append(cirq.CCX(qr_a[i], qr_b[i], ancillary[i]))

    # Measure ancillary qubits
    circuit.append(cirq.measure(*ancillary, key='result'))

    # Simulate
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10000)

    # Build probability distribution
    counts = result.histogram(key='result')
    total = sum(counts.values())
    prob_dist = {}
    for outcome, count in counts.items():
        # Convert integer outcome to 3-bit binary string (little-endian to match Qiskit)
        bits = format(outcome, '03b')
        prob_dist[bits] = count / total

    return prob_dist
