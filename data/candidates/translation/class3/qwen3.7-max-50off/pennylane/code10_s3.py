# EVAL_META: task_id=10, framework=pennylane, class=3
import pennylane as qml

def create_operator():
    with qml.tape.QuantumTape() as tape:
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 0])
        qml.CNOT(wires=[0, 1])
    return tape
