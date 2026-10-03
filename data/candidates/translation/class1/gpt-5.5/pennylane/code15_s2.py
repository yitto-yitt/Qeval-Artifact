# EVAL_META: task_id=15, framework=pennylane, class=1
import pennylane as qml
import numpy as np
from collections import Counter

def noisy_bell():
    shots = 1000
    dev = qml.device("default.mixed", wires=2, shots=shots)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.DepolarizingChannel(0.001, wires=0)
        qml.CNOT(wires=[0, 1])
        qml.DepolarizingChannel(0.01, wires=0)
        qml.DepolarizingChannel(0.01, wires=1)
        qml.BitFlip(0.02, wires=0)
        qml.BitFlip(0.02, wires=1)
        return qml.sample(wires=[0, 1])

    samples = np.asarray(circuit())
    counts = Counter("".join(str(int(bit)) for bit in sample[::-1]) for sample in samples)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
