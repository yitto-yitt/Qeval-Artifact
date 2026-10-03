# EVAL_META: task_id=7, framework=pennylane, class=3
import pennylane as qml


def create_parametrized_gate():
    theta = qml.numpy.array(0.0, requires_grad=True)

    def circuit(param):
        qml.RX(param, wires=0)
        return qml.state()

    dev = qml.device("default.qubit", wires=1)
    qnode = qml.QNode(circuit, dev)
    qnode.theta = theta
    return qnode
