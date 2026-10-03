# EVAL_META: task_id=7, framework=pennylane, class=3
import pennylane as qml
from sympy import Symbol

def create_parametrized_gate():
    theta = Symbol("theta")
    return qml.tape.QuantumScript([qml.RX(theta, wires=0)], [])
