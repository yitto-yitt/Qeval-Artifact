# EVAL_META: task_id=37, framework=cirq, class=1
import cirq


def bv_algorithm(s):
    n = len(s)
    q = cirq.LineQubit.range(n + 1)
    ancilla = q[n]

    circuit = cirq.Circuit()
    circuit.append(cirq.X(ancilla))
    circuit.append(cirq.H.on_each(*q))

    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit.append(cirq.CNOT(q[index], ancilla))

    circuit.append(cirq.H.on_each(*q[:n]))
    circuit.append(cirq.measure(*reversed(q[:n]), key="meas"))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)
    bitstrings = [
        "".join(str(int(bit)) for bit in row)
        for row in result.measurements["meas"]
    ]
    return [bitstrings, result]
