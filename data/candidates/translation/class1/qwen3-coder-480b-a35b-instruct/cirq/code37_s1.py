# EVAL_META: task_id=37, framework=cirq, class=1
import cirq
import numpy as np


def bv_algorithm(s):
    n = len(s)
    qubits = [cirq.LineQubit(i) for i in range(n + 1)]
    ancilla = qubits[n]
    circuit = cirq.Circuit()

    # Initialize ancilla qubit to |1⟩
    circuit.append(cirq.X(ancilla))

    # Apply Hadamard gates to all qubits
    circuit.append(cirq.H.on_each(*qubits))

    # Apply oracle: CX gates based on secret string s
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit.append(cirq.CNOT(qubits[index], ancilla))

    # Apply Hadamard gates to input qubits
    circuit.append(cirq.H.on_each(*qubits[:n]))

    # Measure input qubits
    measurements = []
    for i in range(n):
        measurements.append(cirq.measure(qubits[i], key=f'q{i}'))

    circuit.append(measurements)

    # Run simulation
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)
    
    # Extract bitstrings
    bitstrings = []
    for i in range(1):
        bitstring = ""
        for j in range(n):
            bitstring += str(result.measurements[f'q{j}'][i])
        bitstrings.append(bitstring)

    return [bitstrings, result]
