# EVAL_META: task_id=50, framework=pennylane, class=3

def remove_gate_in_position(circuit, position):
    ops = list(circuit.operations)
    del ops[position]
    circuit._ops = ops
    return circuit
