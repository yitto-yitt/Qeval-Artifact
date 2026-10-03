# EVAL_META: task_id=109, framework=cirq, class=3
import cirq
import sympy

def circuit():
    q = cirq.LineQubit(0)
    theta = sympy.Symbol('th')
    c = cirq.Circuit()
    c.append(cirq.H(q))
    c.append(cirq.rz(theta)(q))
    return c
