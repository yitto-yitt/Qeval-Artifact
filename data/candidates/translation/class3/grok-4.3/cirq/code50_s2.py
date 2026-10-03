# EVAL_META: task_id=50, framework=cirq, class=3
import cirq

def remove_gate_in_position(circuit, position):
    operations = list(circuit.all_operations())
    if 0 <= position < len(operations):
        del operations[position]
    return cirq.Circuit(operations)
