# EVAL_META: task_id=125, framework=cirq, class=3
import cirq


def circ_to_gate(circ):
    # Convert the circuit to a gate by creating a new circuit with the same operations
    # and then converting it to a gate
    return cirq.Circuit(circ.all_operations()).to_op()
