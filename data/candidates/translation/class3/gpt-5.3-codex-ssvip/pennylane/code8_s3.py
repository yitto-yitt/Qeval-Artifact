# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml

def rx_gate(value=None):
    theta = qml.numpy.array(value) if value is not None else qml.numpy.array(0.0, requires_grad=True)

    def circuit():
        qml.RX(theta, wires=0)
        return qml.state()

    return qml.QNode(circuit, qml.device("default.qubit", wires=1))
