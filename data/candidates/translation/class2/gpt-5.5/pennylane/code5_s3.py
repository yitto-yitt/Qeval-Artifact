# EVAL_META: task_id=5, framework=pennylane, class=2
import pennylane as qml
import numpy as np


def create_state_prep():
    return qml.tape.QuantumScript(
        [qml.BasisState(np.array([0, 1]), wires=[0, 1])],
        []
    )
