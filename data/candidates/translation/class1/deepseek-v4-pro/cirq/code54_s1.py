# EVAL_META: task_id=54, framework=cirq, class=1
import cirq

def and_gate(a, b):
    # Convert integers to 3-bit binary strings
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    # Define qubits: 3 for a, 3 for b, 3 ancilla
    a_qubits = cirq.LineQubit.range(0, 3)
    b_qubits = cirq.LineQubit.range(3, 6)
    anc_qubits = cirq.LineQubit.range(6, 9)
    circuit = cirq.Circuit()
    # Initialize a and b registers
    for i, bit in enumerate(a_bin):
        if bit == '1':
            circuit.append(cirq.X(a_qubits[i]))
    for i, bit in enumerate(b_bin):
        if bit == '1':
            circuit.append(cirq.X(b_qubits[i]))
    # Apply Toffoli gates for bitwise AND
    for i in range(3):
        circuit.append(cirq.CCX(a_qubits[i], b_qubits[i], anc_qubits[i]))
    # Measure ancilla qubits (order: MSB to LSB)
    circuit.append(cirq.measure(*anc_qubits, key='result'))
    # Run the circuit
    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions=1024)
    hist = result.histogram(key='result')
    total = sum(hist.values())
    # Convert integer outcomes to 3-bit strings and normalize
    prob_dict = {}
    for outcome, count in hist.items():
        outcome_str = format(outcome, '03b')
        prob_dict[outcome_str] = count / total
    return prob_dict
