# EVAL_META: task_id=99, framework=cirq, class=3
import cirq

def remove_unassigned_parameterized_gates(circuit):
    return cirq.Circuit(
        cirq.Moment(
            operation
            for operation in moment.operations
            if not cirq.is_parameterized(operation)
        )
        for moment in circuit
    )
