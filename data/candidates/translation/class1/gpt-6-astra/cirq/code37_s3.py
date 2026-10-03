# EVAL_META: task_id=37, framework=cirq, class=1
import cirq


def bv_algorithm(s):
    n = len(s)
    qubits = cirq.LineQubit.range(n + 1)
    ancilla = qubits[n]
    circuit = cirq.Circuit(
        cirq.X(ancilla),
        cirq.H.on_each(*qubits),
    )

    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit.append(cirq.CNOT(qubits[index], ancilla))

    circuit.append(cirq.H.on_each(*qubits[:n]))
    if n:
        circuit.append(cirq.measure(*reversed(qubits[:n]), key="meas"))
    else:
        circuit.append(cirq.measure(ancilla, key="ancilla"))

    result = cirq.Simulator().run(circuit, repetitions=1)
    bitstrings = (
        ["".join(str(int(bit)) for bit in row) for row in result.measurements["meas"]]
        if n
        else [""]
    )
    return [bitstrings, result]
