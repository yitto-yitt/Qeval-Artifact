# EVAL_META: task_id=109, framework=pennylane, class=3
import pennylane as qml
import sympy as sp

def circuit():
    theta = sp.Symbol("th")
    ops = [qml.Hadamard(wires=0), qml.RZ(theta, wires=0)]
    return qml.tape.QuantumScript(ops, [qml.state()])
