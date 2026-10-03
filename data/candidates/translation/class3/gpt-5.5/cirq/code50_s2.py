# EVAL_META: task_id=50, framework=cirq, class=3
import cirq

def remove_gate_in_position(circuit, position):
    ops_with_indices = []
    for moment_index, moment in enumerate(circuit):
        for op in moment.operations:
            ops_with_indices.append((moment_index, op))
    if position < 0:
        position += len(ops_with_indices)
    moment_index, op = ops_with_indices[position]
    circuit.batch_remove([(moment_index, op)])
    return circuit
