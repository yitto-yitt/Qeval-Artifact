# EVAL_META: task_id=56, framework=cirq, class=1
import cirq
from collections import Counter

def not_gate(a):
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()
    a = format(a, "08b")
    for i in range(8):
        if a[7 - i] == "0":
            circuit.append(cirq.X(qubits[i]))
    circuit.append(cirq.measure(*qubits, key="meas"))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    measurements = result.measurements["meas"]

    counts = Counter("".join(str(int(bit)) for bit in row[::-1]) for row in measurements)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
