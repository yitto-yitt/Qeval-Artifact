# EVAL_META: task_id=5, framework=pennylane, class=2
import pennylane as qml

def create_state_prep():
    with qml.tape.QuantumTape() as tape:
        qml.BasisState([0, 1], wires=[0, 1])
    return tape
