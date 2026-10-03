# EVAL_META: task_id=55, framework=cirq, class=1
import cirq

def or_gate(a, b):
    # qubits: a0..a2, b0..b2, anc0..anc2
    qa = [cirq.LineQubit(i) for i in range(3)]
    qb = [cirq.LineQubit(3 + i) for i in range(3)]
    qanc = [cirq.LineQubit(6 + i) for i in range(3)]

    circuit = cirq.Circuit()

    # Convert integers to 3-bit binary strings (MSB left)
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')

    # Prepare inputs: set qubit to |1> if bit is '0' (because we will later compute NOT both zeros)
    for i in range(3):
        bit_a = a_bin[2 - i]  # LSB corresponds to i=0
        bit_b = b_bin[2 - i]
        if bit_a == '0':
            circuit.append(cirq.X(qa[i]))
        if bit_b == '0':
            circuit.append(cirq.X(qb[i]))
        # Toffoli to compute AND of complements
        circuit.append(cirq.TOFFOLI(qa[i], qb[i], qanc[i]))

    # Flip ancilla to get OR
    circuit.append(cirq.X.on_each(*qanc))

    # Measure each ancilla qubit individually to control bit ordering
    # anc0 holds LSB, anc1 middle, anc2 MSB. We measure with keys m0,m1,m2.
    for i in range(3):
        circuit.append(cirq.measure(qanc[i], key=f'm{i}'))

    # Simulate with many repetitions
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10000)

    # Reconstruct bitstrings from individual measurements
    counts = {}
    m0_data = result.measurements['m0']
    m1_data = result.measurements['m1']
    m2_data = result.measurements['m2']
    for rep in range(len(m0_data)):
        bit0 = int(m0_data[rep][0])
        bit1 = int(m1_data[rep][0])
        bit2 = int(m2_data[rep][0])
        bitstring = f"{bit2}{bit1}{bit0}"  # MSB on left
        counts[bitstring] = counts.get(bitstring, 0) + 1

    total = sum(counts.values())
    return {key: val / total for key, val in counts.items()}
