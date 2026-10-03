# EVAL_META: task_id=10, framework=pennylane, class=3
import pennylane as qml

def create_operator():
    dev = qml.device("default.qubit", wires=2)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(0)
        qml.PauliX(1)
        return qml.state()

    return qml.transforms.compile(basis_set=["RX", "RY", "RZ", "CNOT"], num_passes=1)(circuit)
