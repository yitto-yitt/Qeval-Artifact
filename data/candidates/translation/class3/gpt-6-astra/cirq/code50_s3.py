# EVAL_META: task_id=50, framework=cirq, class=3
import cirq

def remove_gate_in_position(circuit, position):
    operations = [
        (moment_index, operation)
        for moment_index, moment in enumerate(circuit)
        for operation in moment.operations
    ]
    removals = operations[position]
    if not isinstance(position, slice):
        removals = [removals]
    circuit.batch_remove(removals)
    return circuit
