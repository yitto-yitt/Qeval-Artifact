# EVAL_META: task_id=37, framework=cirq, class=1
import cirq

def bv_algorithm(s):
    n = len(s)
    qubits = cirq.LineQubit.range(n + 1)
    ancilla = qubits[n]
    input_qubits = qubits[:n]

    circuit = cirq.Circuit()
    circuit.append(cirq.X(ancilla))
    circuit.append(cirq.H.on_each(*qubits))

    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit.append(cirq.CX(input_qubits[index], ancilla))

    circuit.append(cirq.H.on_each(*input_qubits))
    circuit.append(cirq.measure(*input_qubits, key='meas'))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)

    measurements = result.measurements['meas']
    bitstrings = [''.join(str(int(b)) for b in row[::-1]) for row in measurements]
    return [bitstrings, result]
