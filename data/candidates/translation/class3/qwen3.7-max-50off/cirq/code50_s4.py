# EVAL_META: task_id=50, framework=cirq, class=3
import cirq

def remove_gate_in_position(circuit, position):
    ops = list(circuit.all_operations())
    if position < 0:
        position += len(ops)
        
    count = 0
    new_moments = []
    for moment in circuit.moments:
        new_ops = []
        for op in moment.operations:
            if count == position:
                count += 1
                continue
            new_ops.append(op)
            count += 1
        if new_ops:
            new_moments.append(cirq.Moment(new_ops))
            
    circuit._moments.clear()
    circuit._moments.extend(new_moments)
    return circuit
