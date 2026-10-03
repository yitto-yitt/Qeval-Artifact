# EVAL_META: task_id=37, framework=cirq, class=1
import cirq

def bv_algorithm(s):
    n = len(s)
    qubits = cirq.LineQubit.range(n + 1)
    ancilla = qubits[n]

    circuit = cirq.Circuit()

    # Step 1: flip ancilla to |1>
    circuit.append(cirq.X(ancilla))

    # Step 2: apply Hadamard to all qubits
    circuit.append(cirq.H.on_each(*qubits))

    # Step 3: apply CNOT from data qubits to ancilla if the corresponding
    #         bit in the reversed secret string s is '1'
    for i, bit in enumerate(reversed(s)):
        if bit == '1':
            circuit.append(cirq.CNOT(qubits[i], ancilla))

    # Step 4: apply Hadamard again to the first n qubits
    circuit.append(cirq.H.on_each(*qubits[:n]))

    # Step 5: measure the first n qubits into the key 'meas'
    circuit.append(cirq.measure(*qubits[:n], key='meas'))

    # Execute the circuit exactly once
    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions=1)

    # Extract the measured bitstring from the result
    # result.measurements['meas'] is a 2D array; we take the first (and only) row
    bitstring = ''.join(str(int(b)) for b in result.measurements['meas'][0])
    bitstrings = [bitstring]

    return [bitstrings, result]
