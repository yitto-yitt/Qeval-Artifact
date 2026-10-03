# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml
import numpy as np
from collections import Counter

def init_random_3qubit(desired_vector):
    dev = qml.device("default.qubit", wires=3, shots=4096, seed=42)

    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(desired_vector, wires=[0, 1, 2])
        return qml.sample(wires=[0, 1, 2])

    samples = np.asarray(circuit())
    counts = Counter("".join(str(int(bit)) for bit in sample) for sample in samples)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
