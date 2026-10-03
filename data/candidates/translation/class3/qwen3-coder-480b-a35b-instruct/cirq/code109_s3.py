# EVAL_META: task_id=109, framework=cirq, class=3
import cirq
import sympy

def circuit():
    qubit = cirq.LineQubit(0)
    theta = sympy.Symbol('th')
    return cirq.Circuit(
        cirq.H(qubit),
        cirq.rz(theta).on(qubit)
    )
