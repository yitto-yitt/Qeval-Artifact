# EVAL_META: task_id=15, framework=pennylane, class=1
import pennylane as qml
from pennylane import numpy as np

def noisy_bell():
    shots = 1000
    dev = qml.device("default.mixed", wires=2, shots=shots)

    p = 0.02

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.DepolarizingChannel(p, wires=0)
        qml.CNOT(wires=[0, 1])
        qml.DepolarizingChannel(p, wires=0)
        qml.DepolarizingChannel(p, wires=1)
        return qml.sample(wires=[0, 1])

    samples = circuit()
    counts = {}
    for s in samples:
        key = "".join(str(int(b)) for b in s)
        counts[key] = counts.get(key, 0) + 1

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
