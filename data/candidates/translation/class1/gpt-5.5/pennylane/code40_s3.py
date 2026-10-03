# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def init_random_3qubit(desired_vector):
    state = np.asarray(desired_vector, dtype=complex)
    dev = qml.device("default.qubit", wires=3, shots=4096, seed=42)

    @qml.qnode(dev)
    def circuit(vec):
        qml.StatePrep(vec, wires=[2, 1, 0])
        return qml.counts(wires=[2, 1, 0], all_outcomes=False)

    counts = circuit(state)
    total = sum(counts.values())
    return {str(key): value / total for key, value in counts.items()}
