# EVAL_META: task_id=8, framework=cirq, class=3
import cirq

def rx_gate(value=None):
    theta = cirq.Symbol("theta")
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    circuit.append(cirq.rx(theta).on(qubit))
    if value is not None:
        resolver = cirq.ParamResolver({"theta": value})
        return cirq.resolve_parameters(circuit, resolver)
    return circuit
