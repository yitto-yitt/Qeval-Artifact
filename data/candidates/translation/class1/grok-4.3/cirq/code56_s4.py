# EVAL_META: task_id=56, framework=cirq, class=1
import cirq
from collections import Counter

def not_gate(a):
    a_bin = format(a, "08b")
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()
    for i in range(8):
        if a_bin[7 - i] == "0":
            circuit.append(cirq.X(qubits[i]))
    circuit.append(cirq.measure(*reversed(qubits), key="result"))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    measurements = result.measurements["result"]
    bitstrings = ["".join(map(str, m)) for m in measurements]
    counts = Counter(bitstrings)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
