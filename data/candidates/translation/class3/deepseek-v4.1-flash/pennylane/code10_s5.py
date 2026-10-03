# EVAL_META: task_id=10, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumTape

def create_operator():
    with QuantumTape() as tape:
        qml.PauliX(wires=0)
        qml.PauliX(wires=1)
    return tape
