# EVAL_META: task_id=7, framework=pennylane, class=3
import pennylane as qml

def create_parametrized_gate():
    theta = "theta"
    return qml.tape.QuantumScript([qml.RX(theta, wires=0)])
