# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np

def remove_unassigned_parameterized_gates(circuit):
    # Extract the operations from the input circuit
    ops = circuit.operations
    
    # Create a new tape without unassigned parameterized gates
    with qml.tape.QuantumTape() as new_tape:
        for op in ops:
            # Check if the operation has parameters that are unassigned (i.e., are Parameter objects)
            has_unassigned_params = False
            
            if hasattr(op, 'parameters'):
                params = op.parameters
                for param in params:
                    if hasattr(param, '__class__') and param.__class__.__name__ == 'Parameter':
                        has_unassigned_params = True
                        break
                    elif isinstance(param, qml.numpy.tensor) and hasattr(param, 'val') and hasattr(param.val, '__class__') and param.val.__class__.__name__ == 'Parameter':
                        has_unassigned_params = True
                        break
            
            # If no unassigned parameters, add to new tape
            if not has_unassigned_params:
                qml.apply(op)
    
    # Copy measurements from original circuit if any
    for m in circuit.measurements:
        qml.apply(m)
    
    return new_tape
