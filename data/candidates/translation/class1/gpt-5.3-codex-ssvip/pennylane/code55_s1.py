# EVAL_META: task_id=55, framework=pennylane, class=1
import pennylane as qml
from pennylane import numpy as np

def or_gate(a, b):
    a_bits = format(a, "03b")
    b_bits = format(b, "03b")

    dev = qml.device("default.qubit", wires=9, shots=1000)

    @qml.qnode(dev)
    def circuit():
        # Wires 0-2: qr_a, 3-5: qr_b, 6-8: ancillary
        for i in range(3):
            if a_bits[2 - i] == "0":
                qml.PauliX(wires=i)
            if b_bits[2 - i] == "0":
                qml.PauliX(wires=3 + i)

        for i in range(3):
            qml.Toffoli(wires=[i, 3 + i, 6 + i])

        for i in range(3):
            qml.PauliX(wires=6 + i)

        return qml.sample(wires=[6, 7, 8])

    samples = circuit()
    counts = {}
    for s in samples:
        bitstring = "".join(str(int(x)) for x in s)
        counts[bitstring] = counts.get(bitstring, 0) + 1

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
