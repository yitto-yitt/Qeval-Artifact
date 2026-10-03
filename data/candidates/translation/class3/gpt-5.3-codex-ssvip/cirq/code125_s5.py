# EVAL_META: task_id=125, framework=cirq, class=3
import cirq


def circ_to_gate(circ):
    if isinstance(circ, cirq.Gate):
        return circ
    if not isinstance(circ, cirq.Circuit):
        raise TypeError("circ must be a cirq.Circuit or cirq.Gate")
    return cirq.CircuitOperation(cirq.FrozenCircuit(circ))
