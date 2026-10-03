# EVAL_META: task_id=106, framework=pennylane, class=3
import pennylane as qml


def compose_cnot_dihedral():
    cx = qml.CNOT(wires=[0, 1])
    t = qml.T(wires=0)
    x = qml.X(wires=1)
    elem1 = t @ cx
    elem2 = x @ t @ cx
    composed_elem = elem1 @ elem2
    return composed_elem
