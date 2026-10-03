# EVAL_META: task_id=40, framework=pennylane, class=1
import numpy as np
import pennylane as qml

def init_random_3qubit(desired_vector):
    dev = qml.device("default.qubit", wires=3, seed=42)

    @qml.set_shots(shots=4096)
    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(
            np.asarray(desired_vector, dtype=complex),
            wires=[2, 1, 0],
            normalize=False,
            validate_norm=True,
        )
        return qml.counts(wires=[2, 1, 0])

    counts = circuit()
    total = sum(int(value) for value in counts.values())
    return {key: int(value) / total for key, value in counts.items()}
