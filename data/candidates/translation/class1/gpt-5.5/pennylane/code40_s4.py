# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def init_random_3qubit(desired_vector):
    state = np.asarray(desired_vector, dtype=complex)
    dev = qml.device("default.qubit", wires=3)

    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(state, wires=[0, 1, 2])
        return qml.probs(wires=[0, 1, 2])

    probs = np.asarray(circuit(), dtype=float)
    probs = probs / float(np.sum(probs))
    return {format(i, "03b"): float(p) for i, p in enumerate(probs) if p > 0.0}
