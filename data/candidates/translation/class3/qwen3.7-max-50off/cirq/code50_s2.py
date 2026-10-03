# EVAL_META: task_id=50, framework=cirq, class=3
import cirq

def remove_gate_in_position(circuit, position):
    flat_ops = list(circuit.all_operations())
    _ = flat_ops[position]
    
    idx = 0
    new_moments = []
    removed = False
    for moment in circuit.moments:
        ops = list(moment.operations)
        orig_len = len(ops)
        if not removed and idx + orig_len > position:
            op_idx = position - idx
            del ops[op_idx]
            removed = True
            if ops:
                new_moments.append(cirq.Moment(ops))
        else:
            if ops:
                new_moments.append(cirq.Moment(ops))
        idx += orig_len
        
    circuit.clear()
    for m in new_moments:
        circuit.append(m, strategy=cirq.InsertStrategy.NEW)
    return circuit
