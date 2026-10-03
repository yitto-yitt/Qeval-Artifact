# EVAL_META: task_id=50, framework=cirq, class=3
import cirq

def remove_gate_in_position(circuit, position):
    operations = list(circuit.all_operations())
    target = operations[position]

    for i, moment in enumerate(circuit.moments):
        if target in moment.operations:
            remaining = [op for op in moment.operations if op != target]
            if remaining:
                circuit[i] = cirq.Moment(remaining)
            else:
                del circuit[i]
            return circuit

    return circuit
