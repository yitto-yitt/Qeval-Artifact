# EVAL_META: task_id=106, framework=pennylane, class=3
import pennylane as qml

def compose_cnot_dihedral():
    with qml.tape.QuantumTape() as tape1:
        qml.CNOT(wires=[0, 1])
        qml.T(wires=0)
    with qml.tape.QuantumTape() as tape2:
        qml.CNOT(wires=[0, 1])
        qml.T(wires=0)
        qml.X(wires=1)
    mat1 = qml.matrix(tape1)
    mat2 = qml.matrix(tape2)
    composed_mat = mat1 @ mat2
    return composed_mat
