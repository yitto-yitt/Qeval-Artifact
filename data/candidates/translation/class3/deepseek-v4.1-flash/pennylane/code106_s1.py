# EVAL_META: task_id=106, framework=pennylane, class=3
import pennylane as qml

def compose_cnot_dihedral():
    with qml.tape.QuantumTape() as tape:
        qml.CNOT(wires=[0, 1])
        qml.T(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.T(wires=0)
        qml.PauliX(wires=1)
    matrix = qml.matrix(tape)
    return qml.QubitUnitary(matrix, wires=[0, 1])
