# EVAL_META: task_id=13, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def custom_rotation_gate():
    U = np.array([[1, -1j], [1j, -1]]) / np.sqrt(2)
    with qml.tape.QuantumTape() as tape:
        qml.QubitUnitary(U, wires=0)
    return tape
