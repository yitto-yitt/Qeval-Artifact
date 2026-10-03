# EVAL_META: task_id=50, framework=pennylane, class=3
import pennylane as qml

def remove_gate_in_position(circuit, position):
    if hasattr(circuit, "operations"):
        del circuit.operations[position]
    elif hasattr(circuit, "_ops"):
        del circuit._ops[position]
    else:
        del circuit[position]
    return circuit
