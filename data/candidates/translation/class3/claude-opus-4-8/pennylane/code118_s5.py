# EVAL_META: task_id=118, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def create_c3sx_circuit():
    SX = np.array([[1 + 1j, 1 - 1j],
                   [1 - 1j, 1 + 1j]]) / 2
    with qml.tape.QuantumTape() as tape:
        qml.ControlledQubitUnitary(SX, control_wires=[0, 1, 2], wires=3)
    return tape
