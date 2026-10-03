# EVAL_META: task_id=50, framework=cirq, class=3
import cirq

def remove_gate_in_position(circuit: cirq.Circuit, position: int) -> cirq.Circuit:
    idx = 0
    for moment_index, moment in enumerate(circuit):
        for op in moment:
            if idx == position:
                circuit.batch_remove([(moment_index, op)])
                return circuit
            idx += 1
    return circuit
