# EVAL_META: task_id=10, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def create_operator():
    U = np.array([[0, 0, 0, 1],
                  [0, 0, 1, 0],
                  [0, 1, 0, 0],
                  [1, 0, 0, 0]], dtype=complex)

    with qml.tape.QuantumTape() as tape:
        qml.QubitUnitary(U, wires=[0, 1])

    decomposed = qml.transforms.decompose(
        tape, gate_set={"CNOT", "RZ", "RY", "RX", "PhaseShift", "GlobalPhase"}
    )[0][0]

    return decomposed
