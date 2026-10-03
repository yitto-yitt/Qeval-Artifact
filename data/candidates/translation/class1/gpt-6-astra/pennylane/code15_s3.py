# EVAL_META: task_id=15, framework=pennylane, class=1
import numpy as np
import pennylane as qml


def noisy_bell():
    device = qml.device("default.mixed", wires=2)

    # Representative superconducting-device noise for the fake-backend model.
    sx_error = 0.0003
    cx_depolarization = 0.012
    readout_errors = (0.025, 0.020)

    paulis = (
        np.eye(2, dtype=complex),
        np.array([[0, 1], [1, 0]], dtype=complex),
        np.array([[0, -1j], [1j, 0]], dtype=complex),
        np.diag([1, -1]).astype(complex),
    )
    cx_kraus = [
        np.sqrt(
            1 - 15 * cx_depolarization / 16
            if i == j == 0
            else cx_depolarization / 16
        ) * np.kron(left, right)
        for i, left in enumerate(paulis)
        for j, right in enumerate(paulis)
    ]

    @qml.qnode(device)
    def circuit():
        # Native-gate decomposition of H, equivalent up to global phase.
        qml.RZ(np.pi / 2, wires=0)
        qml.SX(wires=0)
        qml.DepolarizingChannel(sx_error, wires=0)
        qml.RZ(np.pi / 2, wires=0)

        qml.CNOT(wires=[0, 1])
        qml.QubitChannel(cx_kraus, wires=[0, 1])

        for wire, error in enumerate(readout_errors):
            qml.BitFlip(error, wires=wire)

        # Qiskit measurement strings place qubit 1 before qubit 0.
        return qml.counts(wires=[1, 0])

    counts = qml.set_shots(circuit, shots=1000)()
    total = sum(counts.values())
    return {key: int(value) / total for key, value in counts.items()}
