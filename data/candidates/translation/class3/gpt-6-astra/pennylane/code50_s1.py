# EVAL_META: task_id=50, framework=pennylane, class=3
import pennylane as qml


def remove_gate_in_position(circuit, position):
    operations = list(circuit.operations)
    del operations[position]
    updated = circuit.copy(operations=operations)
    circuit.__dict__.clear()
    circuit.__dict__.update(updated.__dict__)
    return circuit
