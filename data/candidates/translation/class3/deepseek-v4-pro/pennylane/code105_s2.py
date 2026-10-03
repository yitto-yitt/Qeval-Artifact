# EVAL_META: task_id=105, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumTape


def initialize_cnot_dihedral():
    with QuantumTape() as tape:
        qml.CNOT(wires=[0, 1])
        qml.T(wires=0)
    return tape
