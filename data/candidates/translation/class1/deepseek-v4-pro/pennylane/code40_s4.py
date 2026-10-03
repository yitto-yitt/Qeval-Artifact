# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def init_random_3qubit(desired_vector):
    desired_vector = np.asarray(desired_vector, dtype=complex)
    norm = np.linalg.norm(desired_vector)
    if norm > 0:
        desired_vector = desired_vector / norm

    wires = [2, 1, 0]
    dev = qml.device("default.qubit", wires=3)

    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(desired_vector, wires=wires)
        return qml.probs(wires=wires)

    probs = circuit()
    return {format(i, "03b"): float(probs[i]) for i in range(len(probs))}
