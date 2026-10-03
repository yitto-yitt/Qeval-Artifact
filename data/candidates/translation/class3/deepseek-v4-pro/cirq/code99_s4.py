# EVAL_META: task_id=99, framework=cirq, class=3
import cirq

def remove_unassigned_parameterized_gates(circuit):
    filtered_moments = []
    for moment in circuit:
        kept_ops = [op for op in moment.operations if not cirq.is_parameterized(op)]
        if kept_ops:
            filtered_moments.append(cirq.Moment(kept_ops))
    return cirq.Circuit(filtered_moments)
