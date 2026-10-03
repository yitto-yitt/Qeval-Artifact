# EVAL_META: task_id=105, framework=pennylane, class=3
import pennylane as qml


def initialize_cnot_dihedral():
    return qml.prod(qml.T(wires=0), qml.CNOT(wires=[0, 1]))
