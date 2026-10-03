# EVAL_META: task_id=10, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def create_operator():
    unitary = np.array(
        [[0, 0, 0, 1],
         [0, 0, 1, 0],
         [0, 1, 0, 0],
         [1, 0, 0, 0]],
        dtype=complex,
    )
    circuit = qml.tape.QuantumScript(
        [qml.QubitUnitary(unitary, wires=[1, 0])]
    )
    for transform in (
        qml.transforms.unitary_to_rot,
        qml.transforms.cancel_inverses,
        qml.transforms.merge_rotations,
    ):
        circuits, _ = transform(circuit)
        circuit = circuits[0]
    return circuit
