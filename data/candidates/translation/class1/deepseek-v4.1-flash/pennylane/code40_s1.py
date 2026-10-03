# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml
import numpy as np
from collections import Counter

def init_random_3qubit(desired_vector):
    dev = qml.device("default.qubit", wires=3, shots=1024)

    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(np.array(desired_vector, dtype=complex), wires=range(3))
        return qml.sample()

    samples = circuit()
    samples = np.array(samples)
    counts = Counter(tuple(int(bit) for bit in row[::-1]) for row in samples)
    total = sum(counts.values())
    return {"".join(str(b) for b in key): val / total for key, val in counts.items()}
