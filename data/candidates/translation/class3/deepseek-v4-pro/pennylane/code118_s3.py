# EVAL_META: task_id=118, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_c3sx_circuit():
    sx_matrix = np.array([[1 + 1j, 1 - 1j],
                          [1 - 1j, 1 + 1j]], dtype=complex) / 2
    with qml.tape.QuantumTape() as tape:
        qml.ControlledQubitUnitary(
            sx_matrix,
            control_wires=[0, 1, 2],
            wires=[3],
        )
    return tape
