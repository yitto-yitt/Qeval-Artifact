# EVAL_META: task_id=7, framework=cirq, class=3
import cirq
import sympy

def create_parametrized_gate():
    q = cirq.LineQubit(0)
    theta = sympy.Symbol("theta")
    return cirq.Circuit(cirq.rx(theta).on(q))
