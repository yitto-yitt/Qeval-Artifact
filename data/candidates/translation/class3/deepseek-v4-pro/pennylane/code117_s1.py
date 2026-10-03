# EVAL_META: task_id=117, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np

def decompose_unitary(unitary):
    ops = qml.transforms.two_qubit_decomposition(unitary, wires=[0, 1])
    return qml.tape.QuantumScript(ops)
