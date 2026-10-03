# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml


def rx_gate(value=None):
    device = qml.device("default.qubit", wires=1)

    if value is None:
        @qml.qnode(device)
        def circuit(theta):
            qml.RX(theta, wires=0)
            return qml.state()
    else:
        @qml.qnode(device)
        def circuit():
            qml.RX(value, wires=0)
            return qml.state()

    return circuit
