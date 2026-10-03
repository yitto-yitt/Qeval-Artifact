# EVAL_META: task_id=39, framework=pennylane, class=2
import pennylane as qml


def create_uniform_superposition(n):
    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        for wire in range(n):
            qml.Hadamard(wires=wire)
        return qml.state()

    return circuit()
