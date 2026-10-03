# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml

def rx_gate(value=None):
    if value is None:
        theta = qml.numpy.array(0.0, requires_grad=True)

        @qml.qnode(qml.device("default.qubit", wires=1))
        def circuit(theta=theta):
            qml.RX(theta, wires=0)
            return qml.state()

        return circuit
    else:
        @qml.qnode(qml.device("default.qubit", wires=1))
        def circuit():
            qml.RX(value, wires=0)
            return qml.state()

        return circuit
