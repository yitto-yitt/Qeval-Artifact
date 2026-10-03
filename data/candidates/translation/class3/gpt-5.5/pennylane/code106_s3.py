# EVAL_META: task_id=106, framework=pennylane, class=3
import pennylane as qml


def compose_cnot_dihedral():
    circ1 = qml.tape.QuantumScript(
        [
            qml.CNOT(wires=[0, 1]),
            qml.T(wires=0),
        ]
    )

    circ2 = qml.tape.QuantumScript(
        [
            qml.CNOT(wires=[0, 1]),
            qml.T(wires=0),
            qml.PauliX(wires=1),
        ]
    )

    composed_elem = qml.tape.QuantumScript(circ1.operations + circ2.operations)
    return composed_elem
