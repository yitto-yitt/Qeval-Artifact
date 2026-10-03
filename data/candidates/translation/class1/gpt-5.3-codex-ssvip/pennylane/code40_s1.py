# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def init_random_3qubit(desired_vector):
    dev = qml.device("default.qubit", wires=3, shots=1024, seed=42)

    @qml.qnode(dev)
    def circuit(state):
        qml.StatePrep(np.array(state, dtype=np.complex128), wires=[0, 1, 2], normalize=True)
        return qml.counts(wires=[0, 1, 2])

    counts = circuit(desired_vector)
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
