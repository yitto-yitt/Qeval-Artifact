# EVAL_META: task_id=15, framework=pennylane, class=1
import pennylane as qml


def noisy_bell():
    device = qml.device("default.mixed", wires=2)

    @qml.qnode(device)
    def circuit():
        qml.Hadamard(wires=0)
        qml.DepolarizingChannel(0.001, wires=0)
        qml.CNOT(wires=[0, 1])

        # Local gate-noise approximation to the fake-backend simulator.
        for wire in range(2):
            qml.DepolarizingChannel(0.01, wires=wire)
            qml.AmplitudeDamping(0.005, wires=wire)
            qml.PhaseDamping(0.005, wires=wire)

        # Readout errors act immediately before computational-basis sampling.
        qml.BitFlip(0.02, wires=0)
        qml.BitFlip(0.02, wires=1)

        # Qiskit displays classical bits in descending index order.
        return qml.counts(wires=[1, 0])

    counts = qml.set_shots(circuit, shots=1000)()
    total = sum(int(count) for count in counts.values())
    return {str(bits): int(count) / total for bits, count in counts.items()}
