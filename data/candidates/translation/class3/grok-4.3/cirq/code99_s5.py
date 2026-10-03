# EVAL_META: task_id=99, framework=cirq, class=3
import cirq

def remove_unassigned_parameterized_gates(circuit):
    return cirq.Circuit(
        cirq.Moment(op for op in moment if not cirq.is_parameterized(op))
        for moment in circuit
    )
