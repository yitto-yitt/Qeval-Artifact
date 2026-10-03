# EVAL_META: task_id=7, framework=cirq, class=3
import cirq
import sympy

def create_parametrized_gate():
    theta = sympy.Symbol("theta")
    qubit = cirq.LineQubit(0)
    quantum_circuit = cirq.Circuit(cirq.rx(theta).on(qubit))
    return quantum_circuit
