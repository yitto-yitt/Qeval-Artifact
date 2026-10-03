# EVAL_META: task_id=50, framework=cirq, class=3
import cirq

def remove_gate_in_position(circuit, position):
    operations_with_moments = []
    for moment_index, moment in enumerate(circuit):
        for operation in moment.operations:
            operations_with_moments.append((moment_index, operation))
    circuit.batch_remove([operations_with_moments[position]])
    return circuit
