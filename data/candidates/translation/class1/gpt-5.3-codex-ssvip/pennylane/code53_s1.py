# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml
from pennylane import numpy as np

def xor_gate(a, b):
    n = 8
    dev = qml.device("default.qubit", wires=n, shots=1024)

    @qml.qnode(dev)
    def circuit():
        for i in range(n):
            if (a >> i) & 1:
                qml.PauliX(wires=i)
        for i in range(n):
            if (b >> i) & 1:
                qml.PauliX(wires=i)
        return qml.sample(wires=range(n))

    samples = circuit()
    counts = {}
    for s in samples:
        bitstring = "".join(str(int(bit)) for bit in s[::-1])
        counts[bitstring] = counts.get(bitstring, 0) + 1

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
