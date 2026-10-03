# EVAL_META: task_id=37, framework=cirq, class=1
import cirq


def bv_algorithm(s):
    n = len(s)
    qubits = cirq.LineQubit.range(n + 1)
    ancilla = qubits[-1]
    input_qubits = qubits[:-1]

    circuit = cirq.Circuit()

    # Initialize ancilla to |1⟩ (X gate followed by H gate gives |−⟩ state)
    circuit.append(cirq.X(ancilla))
    circuit.append(cirq.H(ancilla))

    # Apply Hadamard to all input qubits
    circuit.append(cirq.H.on_each(*input_qubits))

    # Oracle implementation: apply CX gates based on secret string s
    for i, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit.append(cirq.CNOT(input_qubits[i], ancilla))

    # Apply Hadamard to all input qubits again
    circuit.append(cirq.H.on_each(*input_qubits))

    # Measure all input qubits
    circuit.append(cirq.measure(*input_qubits, key='result'))

    # Simulate the circuit
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)
    
    # Extract bitstrings
    measurements = result.measurements['result']
    bitstring = ''.join(map(str, measurements[0]))
    bitstrings = [bitstring]

    return [bitstrings, result]
