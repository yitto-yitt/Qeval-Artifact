# EVAL_META: task_id=53, framework=cirq, class=1
import cirq
from collections import Counter

def xor_gate(a, b):
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()

    for i in range(8):
        if (a >> i) & 1:
            circuit.append(cirq.X(qubits[i]))

    for i in range(8):
        if (b >> i) & 1:
            circuit.append(cirq.X(qubits[i]))

    circuit.append(cirq.measure(*qubits, key="meas"))

    simulator = cirq.Simulator()
    repetitions = 1024
    result = simulator.run(circuit, repetitions=repetitions)

    counts = Counter(
        "".join(str(int(bit)) for bit in row[::-1])
        for row in result.measurements["meas"]
    )
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
