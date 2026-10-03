# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def rx_gate(value=None):
    theta = value if value is not None else np.pi

    with qml.tape.QuantumTape() as tape:
        qml.RX(theta, wires=0)

    return tape
