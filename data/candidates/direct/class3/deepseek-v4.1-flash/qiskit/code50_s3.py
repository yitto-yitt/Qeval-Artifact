# EVAL_META: task_id=50, framework=qiskit, class=3

def remove_gate_in_position(circuit, position):
    circuit.data.pop(position)
    return circuit
