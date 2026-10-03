# EVAL_META: task_id=106, framework=pennylane, class=3
import pennylane as qml


def compose_cnot_dihedral():
    op1 = qml.CNOT(wires=[0, 1]) @ qml.T(wires=0)
    op2 = qml.CNOT(wires=[0, 1]) @ qml.T(wires=0) @ qml.X(wires=1)
    composed_op = op1 @ op2
    return composed_op
