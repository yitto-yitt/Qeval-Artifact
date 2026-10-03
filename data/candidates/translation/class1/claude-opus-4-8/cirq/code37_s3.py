# EVAL_META: task_id=37, framework=cirq, class=1
import cirq


def bv_algorithm(s):
    n = len(s)
    qubits = [cirq.LineQubit(i) for i in range(n)]
    ancilla = cirq.LineQubit(n)

    circuit = cirq.Circuit()
    circuit.append(cirq.X(ancilla))
    circuit.append(cirq.H(ancilla))
    circuit.append(cirq.H(q) for q in qubits)

    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit.append(cirq.CNOT(qubits[index], ancilla))

    circuit.append(cirq.H(q) for q in qubits)
    circuit.append(cirq.measure(*qubits, key="meas"))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)

    measurements = result.measurements["meas"]
    bitstrings = ["".join(str(int(b)) for b in row) for row in measurements]

    return [bitstrings, result]
