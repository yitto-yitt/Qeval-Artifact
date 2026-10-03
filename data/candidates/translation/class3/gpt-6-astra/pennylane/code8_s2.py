# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml


def rx_gate(value=None):
    device = qml.device("default.qubit", wires=1)

    @qml.qnode(device)
    def circuit(theta=value):
        if theta is None:
            raise ValueError("A value must be supplied for parameter 'theta'.")
        qml.RX(theta, wires=0)
        return qml.state()

    return circuit
