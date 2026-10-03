# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml
import numpy as np


def init_random_3qubit(desired_vector):
    vec = np.asarray(desired_vector, dtype=complex)
    vec = vec / np.linalg.norm(vec)

    dev = qml.device("default.qubit", wires=3, shots=1024)

    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(vec, wires=[0, 1, 2])
        return qml.sample(wires=[0, 1, 2])

    samples = np.asarray(circuit())
    if samples.ndim == 1:
        samples = samples.reshape(-1, 1)

    counts = {}
    for s in samples:
        # Qiskit bitstring convention: qubit 0 is rightmost
        key = ''.join(str(int(b)) for b in s[::-1])
        counts[key] = counts.get(key, 0) + 1

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
