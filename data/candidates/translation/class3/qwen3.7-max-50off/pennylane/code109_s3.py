# EVAL_META: task_id=109, framework=pennylane, class=3
import pennylane as qml

def circuit():
    with qml.tape.QuantumTape() as tape:
        qml.Hadamard(wires=0)
        qml.RZ(0.0, wires=0)
    return tape
