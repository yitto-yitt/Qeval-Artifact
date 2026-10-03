# EVAL_META: task_id=117, framework=pennylane, class=3
import pennylane as qml

def decompose_unitary(unitary):
    return qml.transforms.two_qubit_decomposition(unitary, wires=[0, 1])
