# EVAL_META: task_id=50, framework=cirq, class=3
import cirq

def remove_gate_in_position(circuit, position):
    ops = list(circuit.all_operations())
    if position < 0:
        position += len(ops)
        
    idx = 0
    new_moments = []
    for moment in circuit:
        new_ops = []
        for op in moment.operations:
            if idx != position:
                new_ops.append(op)
            idx += 1
        if new_ops:
            new_moments.append(cirq.Moment(new_ops))
            
    circuit.clear()
    for m in new_moments:
        circuit.append(m)
    return circuit
