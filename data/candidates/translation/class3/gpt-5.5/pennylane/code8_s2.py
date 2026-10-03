# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml

def rx_gate(value=None):
    theta = "theta"
    parameter = theta if value is None else value
    return qml.tape.QuantumScript(ops=[qml.RX(parameter, wires=0)], measurements=[])
