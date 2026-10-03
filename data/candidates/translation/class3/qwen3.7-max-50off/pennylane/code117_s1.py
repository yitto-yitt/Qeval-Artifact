# EVAL_META: task_id=117, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def decompose_unitary(unitary):
    unitary = np.array(unitary)
    with qml.tape.QuantumTape() as tape:
        qml.QubitUnitary(unitary, wires=[0, 1])
    return tape.expand()
