# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml

def remove_unassigned_parameterized_gates(circuit):
    # Extract the operations from the input circuit
    ops = circuit.operations
    
    # Create a new tape to store operations without unassigned parameters
    with qml.tape.QuantumTape() as new_tape:
        for op in ops:
            # Check if the operation has parameters
            if hasattr(op, 'data'):
                params = op.data
                # Check if any parameter is unassigned (i.e., is a trainable parameter)
                unassigned = False
                for param in params:
                    if isinstance(param, qml.numpy.tensor) or hasattr(param, 'requires_grad'):
                        # If it's a PennyLane tensor with requires_grad, it's considered unassigned
                        if getattr(param, 'requires_grad', True):
                            unassigned = True
                            break
                if not unassigned:
                    qml.apply(op)
            else:
                # If no parameters, just apply the operation
                qml.apply(op)
    
    return new_tape
