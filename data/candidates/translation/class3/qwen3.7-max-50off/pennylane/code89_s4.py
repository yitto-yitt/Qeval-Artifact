# EVAL_META: task_id=89, framework=pennylane, class=3
import pennylane as qml

def create_controlled_hgate():
    with qml.tape.QuantumTape() as tape:
        qml.ctrl(qml.Hadamard(wires=2), control=[0, 1])
    return tape
