# EVAL_META: task_id=54, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def and_gate(a, b):
    dev = qml.device("default.qubit", wires=9, shots=1000)

    @qml.qnode(dev)
    def circuit():
        a_bits = format(a, "03b")
        b_bits = format(b, "03b")

        for i in range(3):
            if a_bits[2 - i] == "1":
                qml.PauliX(wires=i)
            if b_bits[2 - i] == "1":
                qml.PauliX(wires=3 + i)

        for i in range(3):
            qml.Toffoli(wires=[i, 3 + i, 6 + i])

        return qml.sample(wires=[6, 7, 8])

    samples = circuit()
    if samples.ndim == 1:
        samples = samples.reshape(1, -1)

    counts = {}
    for s in samples:
        key = "".join(str(int(bit)) for bit in s[::-1])
        counts[key] = counts.get(key, 0) + 1

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
