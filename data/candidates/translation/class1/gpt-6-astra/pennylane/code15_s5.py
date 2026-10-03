# EVAL_META: task_id=15, framework=pennylane, class=1
import numpy as np
import pennylane as qml


def noisy_bell():
    device = qml.device("default.mixed", wires=2)

    paulis = (
        np.eye(2, dtype=complex),
        np.array([[0, 1], [1, 0]], dtype=complex),
        np.array([[0, -1j], [1j, 0]], dtype=complex),
        np.diag([1, -1]).astype(complex),
    )

    # Backend-style gate and readout noise for the local mixed-state simulator.
    single_qubit_error = 0.001
    two_qubit_error = 0.02
    readout_errors = ((0.02, 0.04), (0.025, 0.035))

    entangling_noise = [
        np.sqrt(
            1 - two_qubit_error + two_qubit_error / 16
            if i == 0 and j == 0
            else two_qubit_error / 16
        ) * np.kron(first, second)
        for i, first in enumerate(paulis)
        for j, second in enumerate(paulis)
    ]

    @qml.qnode(device)
    def circuit():
        # RZ-SX-RZ implements the native-gate decomposition of Hadamard.
        qml.RZ(np.pi / 2, wires=0)
        qml.SX(wires=0)
        qml.DepolarizingChannel(single_qubit_error, wires=0)
        qml.RZ(np.pi / 2, wires=0)
        qml.CNOT(wires=[0, 1])
        qml.QubitChannel(entangling_noise, wires=[0, 1])

        for wire, (p01, p10) in enumerate(readout_errors):
            qml.QubitChannel(
                [
                    np.diag([np.sqrt(1 - p01), np.sqrt(1 - p10)]),
                    np.array([[0, 0], [np.sqrt(p01), 0]]),
                    np.array([[0, np.sqrt(p10)], [0, 0]]),
                ],
                wires=wire,
            )

        return qml.counts(wires=[1, 0])

    counts = qml.set_shots(circuit, shots=1000)()
    total = sum(int(count) for count in counts.values())
    return {str(key): int(count) / total for key, count in counts.items()}
