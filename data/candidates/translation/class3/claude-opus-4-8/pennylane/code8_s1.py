# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml

def rx_gate(value=None):
    dev = qml.device("default.qubit", wires=1)

    @qml.qnode(dev)
    def circuit(theta):
        qml.RX(theta, wires=0)
        return qml.state()

    if value is not None:
        return lambda: circuit(value)
    return circuit
