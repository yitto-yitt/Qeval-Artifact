# EVAL_META: task_id=49, framework=pennylane, class=3
import pennylane as qml

def simple_elitzur_vaidman():
    with qml.tape.QuantumTape() as tape:
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.Hadamard(wires=0)
    return tape
