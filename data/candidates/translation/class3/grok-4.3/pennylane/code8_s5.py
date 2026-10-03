# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np

def rx_gate(value=None):
    theta = np.array(0.0, requires_grad=True) if value is None else value
    tape = qml.tape.QuantumTape()
    with tape:
        qml.RX(theta, wires=0)
    return tape
