# EVAL_META: task_id=117, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def decompose_unitary(unitary):
    return qml.QubitUnitary(np.asarray(unitary, dtype=complex), wires=[0, 1]).decomposition()
