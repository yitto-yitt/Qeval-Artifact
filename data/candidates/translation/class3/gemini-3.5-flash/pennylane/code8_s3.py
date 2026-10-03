# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml
import sympy

def rx_gate(value=None):
    theta = sympy.Symbol("theta") if value is None else value
    ops = [qml.RX(theta, wires=0)]
    return qml.tape.QuantumTape(ops)
