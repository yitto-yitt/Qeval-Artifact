# EVAL_META: task_id=5, framework=pennylane, class=2
import pennylane as qml
import numpy as np


def create_state_prep():
    ops = [qml.BasisState(np.array([1, 0]), wires=[0, 1])]
    return qml.tape.QuantumScript(ops, [])
