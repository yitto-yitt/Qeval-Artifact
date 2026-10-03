# EVAL_META: task_id=50, framework=pennylane, class=3
import pennylane as qml

def remove_gate_in_position(circuit, position):
    del circuit._ops[position]
    return circuit
