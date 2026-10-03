# EVAL_META: task_id=7, framework=cirq, class=3
import cirq

def create_parametrized_gate():
    theta = cirq.Symbol("theta")
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    circuit.append(cirq.Rx(rads=theta).on(qubit))
    return circuit
