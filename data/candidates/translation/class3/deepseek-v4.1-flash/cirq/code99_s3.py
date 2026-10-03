# EVAL_META: task_id=99, framework=cirq, class=3
import cirq

def remove_unassigned_parameterized_gates(circuit):
    new_moments = []
    for moment in circuit.moments:
        ops = [op for op in moment.operations if not cirq.is_parameterized(op)]
        if ops:
            new_moments.append(cirq.Moment(ops))
    return cirq.Circuit(new_moments)
