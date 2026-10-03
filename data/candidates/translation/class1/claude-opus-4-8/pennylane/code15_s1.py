# EVAL_META: task_id=15, framework=pennylane, class=1
import pennylane as qml

def noisy_bell():
    shots = 1000
    dev = qml.device("default.mixed", wires=2, shots=shots)

    p = 0.02

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.DepolarizingChannel(p, wires=0)
        qml.CNOT(wires=[0, 1])
        qml.DepolarizingChannel(p, wires=0)
        qml.DepolarizingChannel(p, wires=1)
        return qml.counts(all_outcomes=True)

    counts = circuit()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items() if value > 0}
