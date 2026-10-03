# EVAL_META: task_id=15, framework=pennylane, class=1
from functools import partial
import numpy as np
import pennylane as qml


def noisy_bell():
    device = qml.device("default.mixed", wires=2)

    paulis = [
        np.eye(2, dtype=complex),
        np.array([[0, 1], [1, 0]], dtype=complex),
        np.array([[0, -1j], [1j, 0]], dtype=complex),
        np.diag([1, -1]).astype(complex),
    ]
    error_probability = 0.01
    two_qubit_noise = [
        np.sqrt(1 - error_probability) * np.eye(4, dtype=complex)
    ]
    two_qubit_noise.extend(
        np.sqrt(error_probability / 15) * np.kron(paulis[i], paulis[j])
        for i in range(4)
        for j in range(4)
        if (i, j) != (0, 0)
    )

    @qml.set_shots(shots=1000)
    @qml.qnode(device)
    @partial(qml.transforms.compile, num_passes=1)
    def circuit():
        qml.RZ(np.pi / 2, wires=0)
        qml.SX(wires=0)
        qml.DepolarizingChannel(0.001, wires=0)
        qml.RZ(np.pi / 2, wires=0)

        qml.CNOT(wires=[0, 1])
        qml.QubitChannel(two_qubit_noise, wires=[0, 1])

        qml.BitFlip(0.02, wires=0)
        qml.BitFlip(0.02, wires=1)
        return qml.counts(wires=[1, 0])

    counts = circuit()
    total = sum(int(value) for value in counts.values())
    return {str(key): int(value) / total for key, value in counts.items()}
