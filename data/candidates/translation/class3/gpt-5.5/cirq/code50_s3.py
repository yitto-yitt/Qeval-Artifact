# EVAL_META: task_id=50, framework=cirq, class=3
import cirq

def remove_gate_in_position(circuit, position):
    indexed_ops = []
    for moment_index, moment in enumerate(circuit):
        for op in moment.operations:
            indexed_ops.append((moment_index, op))
    moment_index, op = indexed_ops[position]
    circuit.batch_remove([(moment_index, op)])
    return circuit
