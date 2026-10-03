# EVAL_META: task_id=106, framework=pennylane, class=3
import pennylane as qml


def compose_cnot_dihedral():
    ops_circ1 = [qml.CNOT(wires=[0, 1]), qml.T(wires=0)]
    ops_circ2 = ops_circ1 + [qml.PauliX(wires=1)]
    return qml.tape.QuantumTape(ops_circ1 + ops_circ2, measurements=[])
