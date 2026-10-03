# EVAL_META: task_id=109, framework=cirq, class=3
import cirq
from cirq import Circuit, LineQubit
import sympy

def circuit():
    qubit = LineQubit(0)
    circ = Circuit()
    circ.append(cirq.H(qubit))
    theta = sympy.Symbol('th')
    circ.append(cirq.rz(theta)(qubit))
    return circ
