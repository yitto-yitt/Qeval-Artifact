# EVAL_META: task_id=40, framework=pennylane, class=1
import numpy as np
import pennylane as qml

def init_random_3qubit(desired_vector):
    dev = qml.device("default.qubit", wires=3, shots=4096, seed=42)

    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(np.array(desired_vector, dtype=complex), wires=range(3))
        return qml.counts(wires=range(3))

    counts = circuit()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
