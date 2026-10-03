# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml

def remove_unassigned_parameterized_gates(circuit):
    # Extract the operations from the input circuit
    ops = circuit.operations
    
    # Create a new tape to store the filtered operations
    with qml.tape.QuantumTape() as new_tape:
        for op in ops:
            # Check if the operation has parameters that are unassigned (i.e., they are trainable parameters)
            params = op.parameters
            has_unassigned_params = False
            
            for param in params:
                if isinstance(param, qml.numpy.tensor) or hasattr(param, 'requires_grad'):
                    # If parameter is a PennyLane tensor or has requires_grad attribute, it's considered unassigned
                    if getattr(param, 'requires_grad', True):
                        has_unassigned_params = True
                        break
                elif isinstance(param, qml.pars.ParameterBase):
                    has_unassigned_params = True
                    break
            
            # Only add the operation if it doesn't have unassigned parameters
            if not has_unassigned_params:
                qml.apply(op)
    
    return new_tape
