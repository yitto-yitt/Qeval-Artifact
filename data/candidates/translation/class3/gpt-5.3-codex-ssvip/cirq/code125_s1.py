# EVAL_META: task_id=125, framework=cirq, class=3
import cirq


def circ_to_gate(circ):
    if isinstance(circ, cirq.Gate):
        return circ
    if isinstance(circ, cirq.CircuitOperation):
        return circ.gate
    if not isinstance(circ, cirq.Circuit):
        raise TypeError("circ must be a cirq.Circuit")
    return cirq.CircuitOperation(cirq.FrozenCircuit(circ)).gate
