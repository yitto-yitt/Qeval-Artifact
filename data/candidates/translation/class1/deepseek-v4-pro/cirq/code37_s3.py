# EVAL_META: task_id=37, framework=cirq, class=1
import cirq


def bv_algorithm(s):
    n = len(s)
    qubits = cirq.LineQubit.range(n + 1)
    ancilla = qubits[n]

    circuit = cirq.Circuit()

    # Start with ancilla in |1>
    circuit.append(cirq.X(ancilla))

    # Apply H to all qubits
    circuit.append(cirq.H.on_each(*qubits))

    # Apply CX gates where secret string has '1'
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit.append(cirq.CNOT(qubits[index], ancilla))

    # Apply H to input qubits
    circuit.append(cirq.H.on_each(*qubits[:n]))

    # Measure input qubits
    circuit.append(cirq.measure(*qubits[:n], key="meas"))

    # Simulate
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)

    # Extract bitstrings
    measurements = result.measurements["meas"]
    bitstrings = ["".join(str(b) for b in measurements[0])]

    return [bitstrings, result]
