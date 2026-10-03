# EVAL_META: task_id=117, framework=pennylane, class=3
import numpy as np
import pennylane as qml

def decompose_unitary(unitary):
    unitary = np.asarray(unitary, dtype=complex)
    if unitary.shape != (4, 4):
        raise ValueError("Input unitary must be a 4x4 matrix.")
    with qml.tape.QuantumTape() as tape:
        qml.QubitUnitary(unitary, wires=[0, 1])
    return tape
