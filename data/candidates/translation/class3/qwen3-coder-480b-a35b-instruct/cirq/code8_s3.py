# EVAL_META: task_id=8, framework=cirq, class=3
import cirq

def rx_gate(value=None):
    qubit = cirq.LineQubit(0)
    theta = sympy.Symbol('theta') if value is None else value
    if value is None:
        gate = cirq.Rx(theta).on(qubit)
        circuit = cirq.Circuit(gate)
        return circuit
    else:
        gate = cirq.Rx(value).on(qubit)
        circuit = cirq.Circuit(gate)
        return circuit
