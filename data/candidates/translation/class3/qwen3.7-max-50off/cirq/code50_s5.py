# EVAL_META: task_id=50, framework=cirq, class=3
import cirq

def remove_gate_in_position(circuit, position):
    ops = list(circuit.all_operations())
    del ops[position]
    return cirq.Circuit(ops)
