# EVAL_META: task_id=10, framework=pennylane, class=3
import pennylane as qml

def create_operator():
    dev = qml.device('default.qubit', wires=2)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=0)
        qml.PauliX(wires=1)
        return qml.state()

    return circuit
