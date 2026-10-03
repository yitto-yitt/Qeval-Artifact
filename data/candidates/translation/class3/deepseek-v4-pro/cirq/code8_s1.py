# EVAL_META: task_id=8, framework=cirq, class=3
import cirq
import sympy

def rx_gate(value=None):
    q = cirq.LineQubit(0)
    theta = sympy.Symbol("theta")
    circuit = cirq.Circuit(cirq.rx(theta).on(q))
    if value is not None:
        circuit = cirq.resolve_parameters(circuit, {theta: value})
    return circuit
