# EVAL_META: task_id=37, framework=cirq, class=1
import cirq


def bv_algorithm(s):
    n = len(s)
    qubits = cirq.LineQubit.range(n + 1)
    ancilla = qubits[n]
    circuit = cirq.Circuit()

    circuit.append(cirq.X(ancilla))
    circuit.append(cirq.H.on_each(*qubits))

    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit.append(cirq.CNOT(qubits[index], ancilla))

    circuit.append(cirq.H.on_each(*qubits[:n]))
    circuit.append(cirq.measure(*qubits[:n], key="meas"))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)

    meas_array = result.measurements["meas"]
    bitstrings = ["".join(map(str, row[::-1])) for row in meas_array]

    return [bitstrings, result]
