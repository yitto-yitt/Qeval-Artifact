# EVAL_META: task_id=109, framework=cirq, class=3
import cirq
import sympy

def circuit():
    q0 = cirq.LineQubit(0)
    theta = sympy.Symbol('th')
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.ZPowGate(exponent=theta/np.pi)(q0)
    )
    return circuit
