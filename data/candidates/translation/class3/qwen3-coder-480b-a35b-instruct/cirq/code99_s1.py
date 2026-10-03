# EVAL_META: task_id=99, framework=cirq, class=3
import cirq
import sympy

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = cirq.Circuit()
    
    for moment in circuit:
        new_moment = cirq.Moment()
        for op in moment:
            # Check if the operation has parameters
            if hasattr(op.gate, 'exponent') and isinstance(op.gate.exponent, sympy.Basic):
                # If parameter is not assigned (i.e., still symbolic), skip this gate
                continue
            new_moment = new_moment.with_operation(op)
        if len(new_moment.operations) > 0:
            new_circuit.append(new_moment)
    
    return new_circuit
