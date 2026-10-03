# EVAL_META: task_id=90, framework=pennylane, class=3
import pennylane as qml

def create_custom_controlled():
    dev = qml.device("default.qubit", wires=4)

    @qml.qnode(dev)
    def circuit():
        qml.ctrl(qml.X(wires=1), control=[0, 3])
        qml.ctrl(qml.Hadamard(wires=2), control=[0, 3])
        return qml.state()

    return circuit
