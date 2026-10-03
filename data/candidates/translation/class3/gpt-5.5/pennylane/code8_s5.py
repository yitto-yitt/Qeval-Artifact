# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml
import sympy as sp

def rx_gate(value=None):
    theta = sp.Symbol("theta")
    parameter = theta if value is None else value
    return qml.tape.QuantumScript([qml.RX(parameter, wires=0)])
