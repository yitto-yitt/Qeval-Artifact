# EVAL_META: task_id=106, framework=pennylane, class=3
import pennylane as qml


def compose_cnot_dihedral():
    with qml.tape.QuantumTape() as tape1:
        qml.CNOT(wires=[0, 1])
        qml.T(wires=0)
    elem1 = qml.CNOTDihedral.from_circuit(tape1)

    with qml.tape.QuantumTape() as tape2:
        qml.CNOT(wires=[0, 1])
        qml.T(wires=0)
        qml.X(wires=1)
    elem2 = qml.CNOTDihedral.from_circuit(tape2)

    return elem1.compose(elem2)
