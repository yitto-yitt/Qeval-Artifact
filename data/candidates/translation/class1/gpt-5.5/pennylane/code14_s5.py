# EVAL_META: task_id=14, framework=pennylane, class=1
import pennylane as qml
import numpy as np
from collections import Counter

def bell_each_shot():
    dev = qml.device("default.qubit", wires=2, shots=10)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])

    samples = np.asarray(circuit(), dtype=int)
    counts = Counter("".join(str(bit) for bit in row) for row in samples)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
