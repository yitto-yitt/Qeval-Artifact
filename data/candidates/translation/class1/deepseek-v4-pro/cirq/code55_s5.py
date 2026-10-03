# EVAL_META: task_id=55, framework=cirq, class=1
import cirq
import numpy as np

def or_gate(a, b):
    # Convert inputs to 3-bit binary strings (LSB on qubit 0)
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')

    # Define qubits
    qr_a = [cirq.NamedQubit(f'qr_a{i}') for i in range(3)]
    qr_b = [cirq.NamedQubit(f'qr_b{i}') for i in range(3)]
    ancillary = [cirq.NamedQubit(f'ancillary{i}') for i in range(3)]

    # Build circuit
    circuit = cirq.Circuit()

    # Prepare inputs: flip qubits where classical bit is '0' (because default state is |0⟩)
    for i in range(3):
        if a_bin[2 - i] == '0':
            circuit.append(cirq.X(qr_a[i]))
        if b_bin[2 - i] == '0':
            circuit.append(cirq.X(qr_b[i]))

    # Apply Toffoli gates: ancillary[i] = qr_a[i] OR qr_b[i] = NOT(NOT(a) AND NOT(b))
    for i in range(3):
        circuit.append(cirq.CCX(qr_a[i], qr_b[i], ancillary[i]))

    # Apply X to ancillary to get OR result
    circuit.append([cirq.X(q) for q in ancillary])

    # Measure ancillary qubits
    circuit.append(cirq.measure(*ancillary, key='result'))

    # Simulate
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10000)
    counts = result.histogram(key='result')

    # Convert histogram (int key) to bitstring keys and normalize
    total = sum(counts.values())
    prob_dist = {}
    for outcome, count in counts.items():
        bitstring = format(outcome, '03b')
        prob_dist[bitstring] = count / total

    return prob_dist
