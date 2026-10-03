# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml
import numpy as np
from collections import Counter

def init_random_3qubit(desired_vector):
    np.random.seed(42)
    dev = qml.device("default.qubit", wires=3, shots=1024)
    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(desired_vector, wires=range(3))
        return qml.sample(wires=range(3))
    samples = circuit()
    bitstrings = [''.join(map(str, reversed(s))) for s in samples]
    counts = Counter(bitstrings)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
