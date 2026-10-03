# EVAL_META: task_id=50, framework=cirq, class=3
import cirq

def remove_gate_in_position(circuit, position):
    operations = list(circuit.findall_operations(lambda op: True))
    if position < 0:
        position += len(operations)
    moment_index, operation = operations[position]
    circuit.batch_remove([(moment_index, operation)])
    return circuit
