# EVAL_META: task_id=99, framework=cirq, class=3
import cirq
from typing import Union

def remove_unassigned_parameterized_gates(circuit: cirq.Circuit) -> cirq.Circuit:
    new_circuit = cirq.Circuit()
    
    for moment in circuit:
        new_moment_ops = []
        for op in moment:
            # Check if operation has unassigned parameters
            if hasattr(op, '_has_unitary_') and not op._has_unitary_():
                # For parameterized operations that are not resolved
                continue
            else:
                # Check if it's a parameterized gate with unassigned parameters
                try:
                    # Try to resolve the operation - if it fails due to unassigned params, skip
                    _ = cirq.unitary(op, default=None)
                    new_moment_ops.append(op)
                except:
                    # If there are unassigned parameters, unitary will fail, so skip this op
                    continue
        
        if new_moment_ops:
            new_circuit.append(cirq.Moment(new_moment_ops))
    
    return new_circuit
