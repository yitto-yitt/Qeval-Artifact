# EVAL_META: task_id=7, framework=cirq, class=3
import cirq

def create_parametrized_gate():
    theta = cirq.ParamKey("theta")
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit(cirq.rx(theta).on(qubit))
    return circuit
