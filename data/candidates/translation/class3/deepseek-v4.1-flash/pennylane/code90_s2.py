# EVAL_META: task_id=90, framework=pennylane, class=3
import pennylane as qml

def create_custom_controlled():
    dev = qml.device("default.qubit", wires=4)
    @qml.qnode(dev)
    def circuit():
        qml.ctrl(qml.PauliX, control=[0, 3])(wires=1)
        qml.ctrl(qml.Hadamard, control=[0, 3])(wires=2)
        return qml.state()
    return circuit
