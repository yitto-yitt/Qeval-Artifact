# EVAL_META: task_id=99, framework=cirq, class=3
import cirq


def remove_unassigned_parameterized_gates(circuit):
    new_moments = []
    for moment in circuit:
        new_ops = []
        for op in moment.operations:
            gate = op.gate
            if gate is None:
                new_ops.append(op)
                continue
            if not cirq.is_parameterized(gate):
                new_ops.append(op)
        if new_ops:
            new_moments.append(cirq.Moment(new_ops))
    return cirq.Circuit(new_moments)
