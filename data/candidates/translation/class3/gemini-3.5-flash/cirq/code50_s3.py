# EVAL_META: task_id=50, framework=cirq, class=3
import cirq

def remove_gate_in_position(circuit: cirq.Circuit, position: int) -> cirq.Circuit:
    total_ops = sum(len(moment) for moment in circuit)
    if position < 0:
        position += total_ops
    
    flat_idx = 0
    for m_idx, moment in enumerate(circuit):
        for op in moment:
            if flat_idx == position:
                circuit[m_idx] = moment.without_operations(op)
                if not circuit[m_idx]:
                    del circuit[m_idx]
                return circuit
            flat_idx += 1
    return circuit
