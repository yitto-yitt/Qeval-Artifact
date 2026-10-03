# EVAL_META: task_id=50, framework=qpanda, class=3

def remove_gate_in_position(circuit, position):
    circuit.delete_gate(position)
    return circuit
