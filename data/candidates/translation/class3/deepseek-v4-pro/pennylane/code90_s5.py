# EVAL_META: task_id=90, framework=pennylane, class=3
import pennylane as qml

def create_custom_controlled():
    dev = qml.device('default.qubit', wires=4)

    def custom_target():
        qml.X(wires=1)
        qml.H(wires=2)

    @qml.qnode(dev)
    def circuit():
        qml.ctrl(custom_target, control=[0, 3])()
        return qml.state()

    return circuit
