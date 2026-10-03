# EVAL_META: task_id=50, framework=pennylane, class=3
import pennylane as qml

def remove_gate_in_position(circuit, position):
    ops = circuit.operations
    new_ops = []
    for i, op in enumerate(ops):
        if i != position:
            new_ops.append(op)
    
    # Create new tape with filtered operations
    with qml.tape.QuantumTape() as new_tape:
        for op in new_ops:
            qml.apply(op)
        # Copy over any measurements from the original tape
        for m in circuit.measurements:
            qml.apply(m)
    
    return new_tape
