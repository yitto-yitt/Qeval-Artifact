# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml


def rx_gate(value=None):
    device = qml.device("default.qubit", wires=1)

    @qml.qnode(device)
    def quantum_circuit(theta=value):
        if value is not None:
            theta = value
        if theta is None:
            raise ValueError("A value for parameter 'theta' is required.")
        qml.RX(theta, wires=0)
        return qml.state()

    return quantum_circuit
