# EVAL_META: task_id=125, framework=cirq, class=3
import cirq


def circ_to_gate(circ):
    # Convert the given circuit into a gate equivalent
    # In Cirq, we can wrap a circuit as a composite gate using CircuitOperation
    circuit_operation = cirq.CircuitOperation(circ)
    return circuit_operation.gate
