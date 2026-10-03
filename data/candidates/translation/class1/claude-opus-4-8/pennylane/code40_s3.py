# EVAL_META: task_id=40, framework=pennylane, class=1
import numpy as np
import pennylane as qml

def init_random_3qubit(desired_vector):
    shots = 1024
    dev = qml.device("default.qubit", wires=3, shots=shots, seed=42)

    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(np.array(desired_vector, dtype=complex), wires=range(3))
        return qml.sample(wires=range(3))

    samples = circuit()
    samples = np.atleast_2d(samples)
    counts = {}
    for s in samples:
        key = "".join(str(int(b)) for b in s)
        counts[key] = counts.get(key, 0) + 1
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
