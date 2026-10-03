# EVAL_META: task_id=37, framework=cirq, class=1
import cirq


def bv_algorithm(s):
    n = len(s)
    qubits = cirq.LineQubit.range(n + 1)
    ancilla = qubits[n]
    
    circuit = cirq.Circuit()
    
    # Initialize ancilla to |1⟩
    circuit.append(cirq.X(ancilla))
    
    # Apply Hadamard to all qubits including ancilla
    circuit.append(cirq.H.on_each(*qubits))
    
    # Apply oracle - CX gates based on secret string s
    for i, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit.append(cirq.CX(qubits[i], ancilla))
    
    # Apply Hadamard to input qubits
    circuit.append(cirq.H.on_each(*qubits[:n]))
    
    # Measure input qubits
    circuit.append(cirq.measure(*qubits[:n], key='result'))
    
    # Simulate the circuit
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)
    
    # Extract bitstrings
    measurements = result.measurements['result']
    bitstrings = []
    for measurement in measurements:
        bitstring = ''.join(map(str, measurement))
        bitstrings.append(bitstring)
    
    return [bitstrings, result]
