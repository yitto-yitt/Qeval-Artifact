# EVAL_META: task_id=50, framework=cirq, class=3
import cirq

def remove_gate_in_position(circuit: cirq.Circuit, position: int) -> cirq.Circuit:
    all_ops = list(circuit.all_operations())
    n = len(all_ops)
    if position < 0:
        position += n
    if position < 0 or position >= n:
        raise IndexError("Circuit index out of range")
    
    idx = 0
    for m_idx, moment in enumerate(circuit):
        for op in moment:
            if idx == position:
                circuit.batch_remove([(m_idx, op)])
                return circuit
            idx += 1
    return circuit
