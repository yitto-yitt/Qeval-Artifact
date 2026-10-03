# EVAL_META: task_id=5, framework=pennylane, class=2
import pennylane as qml


def create_state_prep():
    dev = qml.device("default.qubit", wires=[1, 0])

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=0)
        return qml.state()

    return circuit
