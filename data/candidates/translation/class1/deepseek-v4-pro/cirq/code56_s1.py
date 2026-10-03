# EVAL_META: task_id=56, framework=cirq, class=1
import cirq

def not_gate(a):
    # Create 8 qubits in a line (q0..q7)
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()

    # Binary representation of a, 8 bits, MSB first
    a_bin = format(a, '08b')

    # Apply NOT gate: if original bit is '0', flip it using X
    # qubit i corresponds to bit index 7-i (so qubit 0 is LSB)
    for i in range(8):
        if a_bin[7 - i] == '0':
            circuit.append(cirq.X(qubits[i]))

    # Measure in order: qubit 7 (MSB) first, down to qubit 0 (LSB)
    # This ensures the resulting integer bitstring has the correct endianness
    circuit.append(cirq.measure(qubits[7], qubits[6], qubits[5], qubits[4],
                               qubits[3], qubits[2], qubits[1], qubits[0],
                               key='result'))

    # Simulate multiple shots to obtain a probability distribution
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)

    hist = result.histogram(key='result')
    total = sum(hist.values())

    # Convert integer outcomes to zero-padded 8-bit strings
    return {format(k, '08b'): v / total for k, v in hist.items()}
