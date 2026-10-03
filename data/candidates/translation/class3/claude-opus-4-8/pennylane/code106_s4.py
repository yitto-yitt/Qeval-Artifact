# EVAL_META: task_id=106, framework=pennylane, class=3
import pennylane as qml


def compose_cnot_dihedral():
    # First element: cx(0,1), t(0)
    elem1 = [
        qml.CNOT(wires=[0, 1]),
        qml.T(wires=0),
    ]
    # Second element: cx(0,1), t(0), x(1)
    elem2 = [
        qml.CNOT(wires=[0, 1]),
        qml.T(wires=0),
        qml.PauliX(wires=1),
    ]
    # Composition: apply elem1 followed by elem2
    composed_elem = elem1 + elem2
    return composed_elem
