# EVAL_META: task_id=50, framework=cirq, class=3
import cirq

def remove_gate_in_position(circuit, position):
    del circuit[position]
    return circuit
