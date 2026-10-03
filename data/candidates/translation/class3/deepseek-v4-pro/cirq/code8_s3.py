# EVAL_META: task_id=8, framework=cirq, class=3
import cirq
import sympy

def rx_gate(value=None):
    theta = sympy.Symbol("theta")
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit(cirq.rx(theta)(qubit))
    if value is not None:
        return circuit.resolve_parameters({theta: value})
    return circuit
