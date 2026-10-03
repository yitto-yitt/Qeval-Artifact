# EVAL_META: task_id=5, framework=pennylane, class=2
import pennylane as qml


def create_state_prep():
    return qml.tape.QuantumScript([qml.BasisState([1, 0], wires=[0, 1])])
