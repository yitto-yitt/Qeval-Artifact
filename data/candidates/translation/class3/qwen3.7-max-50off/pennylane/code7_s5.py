# EVAL_META: task_id=7, framework=pennylane, class=3
import pennylane as qml

def create_parametrized_gate():
    theta = 0.0
    with qml.tape.QuantumTape() as tape:
        qml.RX(theta, wires=0)
    return tape
