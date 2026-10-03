# EVAL_META: task_id=15, framework=pennylane, class=1
import pennylane as qml
import numpy as np


def noisy_bell():
    device = qml.device("default.mixed", wires=2)

    @qml.set_shots(shots=1000)
    @qml.qnode(device)
    def circuit():
        # Native-gate decomposition of the Bell-state preparation.
        qml.RZ(np.pi / 2, wires=0)
        qml.SX(wires=0)
        qml.DepolarizingChannel(0.001, wires=0)
        qml.RZ(np.pi / 2, wires=0)
        qml.CNOT(wires=[0, 1])

        # Local hardware-noise approximation for the fake-device execution.
        for wire in range(2):
            qml.DepolarizingChannel(0.01, wires=wire)
            qml.AmplitudeDamping(0.005, wires=wire)

        # Computational-basis readout errors.
        qml.BitFlip(0.025, wires=0)
        qml.BitFlip(0.035, wires=1)
        return qml.sample(wires=[1, 0])

    samples = np.asarray(circuit(), dtype=int)
    outcomes, counts = np.unique(samples, axis=0, return_counts=True)
    total = int(counts.sum())
    return {
        "".join(str(int(bit)) for bit in outcome): int(count) / total
        for outcome, count in zip(outcomes, counts)
    }
