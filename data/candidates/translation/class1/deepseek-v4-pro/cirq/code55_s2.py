# EVAL_META: task_id=55, framework=cirq, class=1
import cirq
import numpy as np

def or_gate(a, b):
    # Convert inputs to 3-bit binary strings
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')

    # Define qubits: 3 for a, 3 for b, 3 for ancillary (result)
    qr_a = [cirq.NamedQubit(f'qr_a_{i}') for i in range(3)]
    qr_b = [cirq.NamedQubit(f'qr_b_{i}') for i in range(3)]
    ancillary = [cirq.NamedQubit(f'ancillary_{i}') for i in range(3)]

    # Build the circuit
    circuit = cirq.Circuit()

    # Prepare input states: flip qubits where bit is '0' (so |0> represents 1, |1> represents 0)
    # Qiskit uses little-endian: a[2-i] corresponds to qubit i
    for i in range(3):
        if a_bin[2 - i] == '0':
            circuit.append(cirq.X(qr_a[i]))
        if b_bin[2 - i] == '0':
            circuit.append(cirq.X(qr_b[i]))

    # Apply Toffoli (CCX) gates: ancillary[i] = qr_a[i] AND qr_b[i]
    for i in range(3):
        circuit.append(cirq.CCX(qr_a[i], qr_b[i], ancillary[i]))

    # Apply X gates on ancillary to get OR (since OR = NOT( (NOT a) AND (NOT b) ))
    circuit.append([cirq.X(ancillary[i]) for i in range(3)])

    # Measure ancillary qubits
    circuit.append(cirq.measure(*ancillary, key='result'))

    # Simulate
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10000)
    counts = result.histogram(key='result')

    # Convert histogram to probability distribution with 3-bit string keys
    total = sum(counts.values())
    prob_dist = {}
    for outcome, count in counts.items():
        # Format outcome as 3-bit binary string (little-endian: ancillary[0] is LSB)
        key = format(outcome, '03b')
        prob_dist[key] = count / total

    return prob_dist
