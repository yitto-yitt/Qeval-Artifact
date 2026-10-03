# EVAL_META: task_id=106, framework=pennylane, class=3
import pennylane as qml


def compose_cnot_dihedral():
    # First circuit as a list of operations: CX(0,1), T(0)
    circ1 = [qml.CNOT(wires=[0, 1]), qml.T(wires=0)]
    # Second circuit: same as first plus an X on qubit 1
    circ2 = [qml.CNOT(wires=[0, 1]), qml.T(wires=0), qml.PauliX(wires=1)]
    # Composition applies circ1 first, then circ2
    composed_elem = circ1 + circ2
    return composed_elem
