# EVAL_META: task_id=15, framework=pennylane, class=1
import pennylane as qml


def noisy_bell():
    dev = qml.device("default.mixed", wires=2)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.DepolarizingChannel(0.005, wires=0)
        qml.CNOT(wires=[0, 1])
        qml.DepolarizingChannel(0.02, wires=0)
        qml.DepolarizingChannel(0.02, wires=1)
        return qml.probs(wires=[0, 1])

    probs = circuit()
    keys = ["00", "01", "10", "11"]
    return {k: float(p) for k, p in zip(keys, probs)}
