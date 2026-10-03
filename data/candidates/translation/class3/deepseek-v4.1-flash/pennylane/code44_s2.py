# EVAL_META: task_id=44, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumTape

def tensor_circuits():
    with QuantumTape() as tape:
        qml.CRY(0.2, wires=[0, 1])
        qml.PauliX(wires=2)
    return tape
