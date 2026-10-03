# EVAL_META: task_id=7, framework=cirq, class=3
import cirq
import sympy

def create_parametrized_gate():
    theta = sympy.Symbol("theta")
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    circuit.append(cirq.rx(theta)(q))
    return circuit
