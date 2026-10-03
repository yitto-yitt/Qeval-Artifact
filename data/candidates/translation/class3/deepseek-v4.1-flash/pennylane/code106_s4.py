# EVAL_META: task_id=106, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumScript


def compose_cnot_dihedral():
    ops = [
        qml.CNOT(wires=[0, 1]),
        qml.T(wires=0),
        qml.CNOT(wires=[0, 1]),
        qml.T(wires=0),
        qml.PauliX(wires=1),
    ]
    tape = QuantumScript(ops, [])
    U = qml.matrix(tape)
    return qml.QubitUnitary(U, wires=[0, 1])
