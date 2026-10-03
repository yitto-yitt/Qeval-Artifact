# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml
import sympy as sp

def rx_gate(value=None):
    theta = sp.Symbol("theta")
    parameter = value if value is not None else theta
    return qml.tape.QuantumScript([qml.RX(parameter, wires=0)], [])
