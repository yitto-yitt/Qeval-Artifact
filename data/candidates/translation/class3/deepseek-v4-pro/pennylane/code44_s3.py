# EVAL_META: task_id=44, framework=pennylane, class=3
import pennylane as qml

def tensor_circuits():
    with qml.tape.QuantumTape() as tape:
        qml.CRY(0.2, wires=[0, 1])
        qml.PauliX(wires=2)
    return tape
