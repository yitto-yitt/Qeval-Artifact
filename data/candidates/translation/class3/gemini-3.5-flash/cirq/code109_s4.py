# EVAL_META: task_id=109, framework=cirq, class=3
import cirq
import sympy

def circuit():
    qubit = cirq.LineQubit(0)
    c = cirq.Circuit()
    c.append(cirq.H(qubit))
    theta = sympy.Symbol('th')
    c.append(cirq.rz(theta)(qubit))
    return c
