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
        qml.probs(wires=circuit.wires)  # Add a measurement to make it a proper tape
    
    # Remove the probs operation we added just to create a valid tape
    new_tape._ops = new_tape.operations[:-1]
    
    return new_tape
