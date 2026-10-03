# EVAL_META: task_id=106, framework=pennylane, class=3
import pennylane as qml

def compose_cnot_dihedral():
    elem1 = qml.T(wires=0) @ qml.CNOT(wires=[0, 1])
    elem2 = qml.X(wires=1) @ qml.T(wires=0) @ qml.CNOT(wires=[0, 1])
    composed_elem = elem1 @ elem2
    return composed_elem
