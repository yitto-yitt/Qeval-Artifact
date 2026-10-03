# EVAL_META: task_id=7, framework=cirq, class=3
import sympy
import cirq

def create_parametrized_gate():
    theta = sympy.Symbol('theta')
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit(cirq.rx(theta).on(q))
    return circuit
