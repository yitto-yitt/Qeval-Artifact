# EVAL_META: task_id=37, framework=cirq, class=1
import cirq


def bv_algorithm(s):
    n = len(s)
    qubits = cirq.LineQubit.range(n + 1)
    input_qubits = qubits[:n]
    ancilla = qubits[n]

    circuit = cirq.Circuit()
    circuit.append(cirq.X(ancilla))
    for q in qubits:
        circuit.append(cirq.H(q))

    for index, bit in enumerate(reversed(s)):
        if bit == '1':
            circuit.append(cirq.CNOT(qubits[index], ancilla))

    for q in input_qubits:
        circuit.append(cirq.H(q))

    if n > 0:
        circuit.append(cirq.measure(*input_qubits, key='meas'))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)

    if n == 0:
        bitstrings = ['']
    else:
        measurement = result.measurements['meas']
        bitstrings = [''.join(str(int(b)) for b in row[::-1]) for row in measurement]

    return [bitstrings, result]
