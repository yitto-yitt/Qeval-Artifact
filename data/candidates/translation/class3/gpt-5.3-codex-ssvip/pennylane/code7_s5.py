# EVAL_META: task_id=7, framework=pennylane, class=3
import pennylane as qml


def create_parametrized_gate():
    theta = qml.numpy.array(0.0, requires_grad=True)

    def circuit(param):
        qml.RX(param, wires=0)
        return qml.state()

    return qml.QNode(circuit, qml.device("default.qubit", wires=1))
