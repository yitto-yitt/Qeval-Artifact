# EVAL_META: task_id=60, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumTape

def create_cy_gate():
    with QuantumTape() as tape:
        qml.adjoint(qml.S)(wires=1)
        qml.CNOT(wires=[0, 1])
        qml.S(wires=1)
    return tape
