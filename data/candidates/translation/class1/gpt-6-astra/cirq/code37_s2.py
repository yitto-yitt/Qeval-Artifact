# EVAL_META: task_id=37, framework=cirq, class=1
import cirq


def bv_algorithm(s):
    n = len(s)
    qubits = cirq.LineQubit.range(n + 1)
    inputs = qubits[:n]
    ancilla = qubits[n]

    circuit = cirq.Circuit()
    circuit.append(cirq.X(ancilla))
    circuit.append(cirq.H.on_each(*qubits))
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit.append(cirq.CNOT(inputs[index], ancilla))
    circuit.append(cirq.H.on_each(*inputs))
    circuit.append(cirq.measure(*reversed(inputs), key="meas"))

    result = cirq.Simulator().run(circuit, repetitions=1)
    bitstrings = [
        "".join(str(int(bit)) for bit in row)
        for row in result.measurements["meas"]
    ]
    return [bitstrings, result]
