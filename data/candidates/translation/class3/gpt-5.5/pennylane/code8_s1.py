# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml

def rx_gate(value=None):
    theta = "theta" if value is None else value
    return qml.tape.QuantumScript([qml.RX(theta, wires=0)], [])
