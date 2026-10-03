# EVAL_META: task_id=109, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np

def circuit():
    theta = np.array(0.0, requires_grad=True)
    with qml.tape.QuantumTape() as tape:
        qml.Hadamard(wires=0)
        qml.RZ(theta, wires=0)
    return tape
