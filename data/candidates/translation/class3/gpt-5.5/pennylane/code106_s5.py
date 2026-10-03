# EVAL_META: task_id=106, framework=pennylane, class=3
import pennylane as qml


def compose_cnot_dihedral():
    circ1_ops = [
        qml.CNOT(wires=[0, 1]),
        qml.T(wires=0),
    ]
    circ2_ops = [
        qml.CNOT(wires=[0, 1]),
        qml.T(wires=0),
        qml.PauliX(wires=1),
    ]
    return qml.tape.QuantumScript(circ1_ops + circ2_ops)
