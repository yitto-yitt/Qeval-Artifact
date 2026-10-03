# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np

def remove_unassigned_parameterized_gates(circuit):
    # Extract the operations from the input circuit
    ops = circuit.operations
    
    # Create a new tape/quantum function without unassigned parameterized gates
    def new_circuit():
        for op in ops:
            # Check if the operation has parameters
            if hasattr(op, 'parameters'):
                params = op.parameters
                # Check if any parameter is unassigned (not a concrete value)
                unassigned = False
                for param in params:
                    if isinstance(param, qml.numpy.tensor) or hasattr(param, '_value') and param._value is None:
                        unassigned = True
                        break
                    elif isinstance(param, type(qml.numpy.array(0.0))) and param.requires_grad:
                        # If it's a trainable parameter, consider it unassigned
                        unassigned = True
                        break
                    elif callable(param):  # If it's a parameter that needs to be evaluated
                        unassigned = True
                        break
                if not unassigned:
                    qml.apply(op)
            else:
                # If no parameters, just apply the operation
                qml.apply(op)
    
    # Create a new tape from the function
    dev = qml.device('default.qubit', wires=circuit.wires)
    with qml.tape.QuantumTape() as new_tape:
        new_circuit()
    
    return new_tape
