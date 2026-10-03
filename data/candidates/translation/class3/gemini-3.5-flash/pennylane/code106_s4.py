# EVAL_META: task_id=106, framework=pennylane, class=3
import pennylane as qml


def compose_cnot_dihedral():
    ops1 = [qml.CNOT(wires=[0, 1]), qml.T(wires=0)]
    ops2 = [qml.CNOT(wires=[0, 1]), qml.T(wires=0), qml.X(wires=1)]
    return qml.tape.QuantumTape(ops1 + ops2)
