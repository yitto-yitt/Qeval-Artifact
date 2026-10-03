# EVAL_META: task_id=5, framework=pennylane, class=2
import pennylane as qml


def create_state_prep():
    device = qml.device("default.qubit", wires=2)

    @qml.qnode(device)
    def circuit():
        qml.PauliX(wires=1)
        return qml.state()

    return circuit
