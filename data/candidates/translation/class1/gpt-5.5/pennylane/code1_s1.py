# EVAL_META: task_id=1, framework=pennylane, class=1
import pennylane as qml


def run_bell_state_simulator():
    dev = qml.device("default.qubit", wires=2, shots=1000)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.probs(wires=[0, 1])

    probs = circuit()
    bitstrings = ["00", "01", "10", "11"]
    return {bitstrings[i]: float(p) for i, p in enumerate(probs) if p > 0}
