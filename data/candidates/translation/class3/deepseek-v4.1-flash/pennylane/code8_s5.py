# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml

def rx_gate(value=None):
    dev = qml.device("default.qubit", wires=1)
    if value is None:
        @qml.qnode(dev)
        def circuit(theta):
            qml.RX(theta, wires=0)
            return qml.state()
        return circuit
    else:
        @qml.qnode(dev)
        def circuit():
            qml.RX(value, wires=0)
            return qml.state()
        return circuit
