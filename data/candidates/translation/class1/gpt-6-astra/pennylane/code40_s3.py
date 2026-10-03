# EVAL_META: task_id=40, framework=pennylane, class=1
import numpy as np
import pennylane as qml

def init_random_3qubit(desired_vector):
    device = qml.device("default.qubit", wires=3, seed=42)

    @qml.qnode(device)
    def circuit():
        qml.StatePrep(
            np.asarray(desired_vector, dtype=complex),
            wires=[0, 1, 2],
            normalize=False,
            validate_norm=True,
        )
        return qml.counts(wires=[0, 1, 2])

    counts = qml.set_shots(circuit, shots=4096)()
    total = sum(counts.values())
    return {key: float(value / total) for key, value in counts.items()}
