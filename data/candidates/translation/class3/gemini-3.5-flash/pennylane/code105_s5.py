# EVAL_META: task_id=105, framework=pennylane, class=3
import pennylane as qml


def initialize_cnot_dihedral():
    # In Qiskit, the circuit applies CX(0, 1) then T(0).
    # The corresponding operator is T(0) @ CNOT(0, 1).
    return qml.prod(qml.T(wires=0), qml.CNOT(wires=[0, 1]))
