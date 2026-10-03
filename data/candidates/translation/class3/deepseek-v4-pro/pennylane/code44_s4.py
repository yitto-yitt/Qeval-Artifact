# EVAL_META: task_id=44, framework=pennylane, class=3
import pennylane as qml

def tensor_circuits():
    dev = qml.device('default.qubit', wires=3)

    @qml.qnode(dev)
    def circuit():
        qml.CRY(0.2, wires=[0, 1])
        qml.X(wires=2)
        return qml.state()

    return circuit
