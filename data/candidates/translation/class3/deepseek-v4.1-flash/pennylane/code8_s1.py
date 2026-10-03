# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml

def rx_gate(value=None):
    if value is not None:
        return qml.RX(value, wires=0)
    return qml.RX(qml.numpy.array(0.0, requires_grad=True), wires=0)
