# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml

def rx_gate(value=None):
    theta = value if value is not None else "theta"
    return qml.tape.QuantumScript([qml.RX(theta, wires=0)])
