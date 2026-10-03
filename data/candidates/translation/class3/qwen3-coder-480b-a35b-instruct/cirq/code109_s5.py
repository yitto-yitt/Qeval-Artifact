# EVAL_META: task_id=109, framework=cirq, class=3
import cirq
from cirq import Circuit, LineQubit
import sympy

def circuit():
    qubit = LineQubit(0)
    theta = sympy.Symbol('th')
    circ = Circuit()
    circ.append(cirq.H(qubit))
    circ.append(cirq.rz(theta).on(qubit))
    return circ
