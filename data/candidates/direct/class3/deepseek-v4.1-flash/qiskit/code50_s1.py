# EVAL_META: task_id=50, framework=qiskit, class=3

def remove_gate_in_position(circuit, position):
    new_circuit = circuit.copy()
    del new_circuit.data[position]
    return new_circuit
