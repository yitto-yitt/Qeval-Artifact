# EVAL_META: task_id=10, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_operator():
    U = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]])
    with qml.tape.QuantumTape() as tape:
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 0])
        qml.CNOT(wires=[0, 1])
    return tape
