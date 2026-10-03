# EVAL_META: task_id=1, framework=pennylane, class=1
import pennylane as qml


def run_bell_state_simulator():
    dev = qml.device("default.qubit", wires=2)

    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.probs(wires=[0, 1])

    probs = bell_circuit()
    bitstrings = ["00", "01", "10", "11"]
    return {bitstrings[i]: float(probs[i]) for i in range(len(bitstrings)) if float(probs[i]) != 0.0}
