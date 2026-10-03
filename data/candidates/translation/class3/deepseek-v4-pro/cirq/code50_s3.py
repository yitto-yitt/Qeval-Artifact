# EVAL_META: task_id=50, framework=cirq, class=3
import cirq

def remove_gate_in_position(circuit, position):
    ops = list(circuit.all_operations())
    if position < 0:
        position += len(ops)
    if position < 0 or position >= len(ops):
        raise IndexError("position out of range")

    linear_index = 0
    for moment_index, moment in enumerate(circuit):
        for op_index in range(len(moment)):
            if linear_index == position:
                circuit.batch_remove([(moment_index, op_index)])
                return circuit
            linear_index += 1

    raise IndexError("position out of range")
