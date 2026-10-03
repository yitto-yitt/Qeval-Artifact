# EVAL_META: task_id=2, framework=pennylane, class=2
import pennylane as qml


def create_bell_statevector():
    device = qml.device("default.qubit", wires=2)

    @qml.qnode(device)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.state()

    return circuit()
