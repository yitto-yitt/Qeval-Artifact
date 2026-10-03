# EVAL_META: task_id=125, framework=cirq, class=3
import cirq


def circ_to_gate(circ: cirq.Circuit) -> cirq.CircuitGate:
    return cirq.CircuitGate(circ)
