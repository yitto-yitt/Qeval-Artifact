# EVAL_META: task_id=125, framework=cirq, class=3
import cirq


def circ_to_gate(circ):
    # Convert Cirq Circuit to a composite gate
    return cirq.CircuitOperation(circ.freeze())
