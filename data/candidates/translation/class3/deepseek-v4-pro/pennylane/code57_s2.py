# EVAL_META: task_id=57, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumTape

def create_swap_gate():
    with QuantumTape() as tape:
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 0])
        qml.CNOT(wires=[0, 1])
    return tape
