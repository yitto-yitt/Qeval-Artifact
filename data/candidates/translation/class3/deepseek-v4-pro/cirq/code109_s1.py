# EVAL_META: task_id=109, framework=cirq, class=3
import cirq
import sympy

def circuit():
    th = sympy.Symbol('th')
    q = cirq.LineQubit(0)
    return cirq.Circuit([cirq.H(q), cirq.rz(th)(q)])
