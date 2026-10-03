# EVAL_META: task_id=105, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def initialize_cnot_dihedral():
    def circuit():
        qml.CNOT(wires=[0, 1])
        qml.T(wires=0)
    mat = qml.matrix(circuit, wire_order=[0, 1])()
    return qml.QubitUnitary(mat, wires=[0, 1])
