# EVAL_META: task_id=117, framework=pennylane, class=3
import pennylane as qml
from pennylane.transforms.decompositions import two_qubit_decomposition

def decompose_unitary(unitary):
    return two_qubit_decomposition(unitary, wires=[0, 1])
