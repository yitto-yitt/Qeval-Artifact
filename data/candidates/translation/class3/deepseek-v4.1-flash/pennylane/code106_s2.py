# EVAL_META: task_id=106, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def compose_cnot_dihedral():
    with qml.tape.QuantumTape() as tape:
        qml.CNOT(wires=[0, 1])
        qml.T(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.T(wires=0)
        qml.PauliX(wires=1)
    U = qml.matrix(tape, wire_order=[0, 1])
    return qml.QubitUnitary(U, wires=[0, 1])
