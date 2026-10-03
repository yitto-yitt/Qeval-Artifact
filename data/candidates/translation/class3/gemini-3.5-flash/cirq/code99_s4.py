# EVAL_META: task_id=99, framework=cirq, class=3
import cirq

def remove_unassigned_parameterized_gates(circuit: cirq.Circuit) -> cirq.Circuit:
    new_moments = []
    for moment in circuit:
        new_ops = [op for op in moment if not cirq.is_parameterized(op)]
        new_moments.append(cirq.Moment(new_ops))
    return cirq.Circuit(new_moments)
