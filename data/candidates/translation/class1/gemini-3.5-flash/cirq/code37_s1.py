# EVAL_META: task_id=37, framework=cirq, class=1
import cirq


def bv_algorithm(s):
    n = len(s)
    qubits = cirq.LineQubit.range(n + 1)
    circuit = cirq.Circuit()

    # State preparation
    circuit.append(cirq.X(qubits[n]))
    circuit.append(cirq.H.on_each(*qubits))

    # Oracle
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit.append(cirq.CNOT(qubits[index], qubits[n]))

    # Measurement preparation
    circuit.append(cirq.H.on_each(*qubits[:n]))

    # Measurement in reverse order to match Qiskit's big-endian bitstring representation
    circuit.append(cirq.measure(*qubits[:n][::-1], key="meas"))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, shots=1)

    # Extract bitstrings
    measurements = result.measurements["meas"]
    bitstrings = ["".join(map(str, row)) for row in measurements]

    return [bitstrings, result]
