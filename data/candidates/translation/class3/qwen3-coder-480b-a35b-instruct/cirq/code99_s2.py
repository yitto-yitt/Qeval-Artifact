# EVAL_META: task_id=99, framework=cirq, class=3
import cirq

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = cirq.Circuit()
    
    for moment in circuit.moments:
        for op in moment.operations:
            # Check if operation has unassigned parameters
            has_unassigned_param = False
            
            # For parameterized gates, check if they have unassigned parameters
            if hasattr(op.gate, '_exponent') and isinstance(op.gate._exponent, cirq.Symbol):
                has_unassigned_param = True
            elif hasattr(op.gate, '_exponent') and hasattr(op.gate._exponent, 'free_symbols') and len(getattr(op.gate._exponent, 'free_symbols', set())) > 0:
                has_unassigned_param = True
            elif hasattr(op, 'params') and any(isinstance(p, cirq.Symbol) for p in getattr(op, 'params', [])):
                has_unassigned_param = True
            elif hasattr(op.gate, '__dict__'):
                # Check for any attribute that might contain symbols
                for attr_name, attr_value in op.gate.__dict__.items():
                    if isinstance(attr_value, cirq.Symbol) or (hasattr(attr_value, 'free_symbols') and len(getattr(attr_value, 'free_symbols', set())) > 0):
                        has_unassigned_param = True
                        break
            
            if not has_unassigned_param:
                new_circuit.append(op)
    
    return new_circuit
