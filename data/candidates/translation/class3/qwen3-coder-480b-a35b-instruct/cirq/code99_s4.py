# EVAL_META: task_id=99, framework=cirq, class=3
import cirq
from typing import List, Any

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = cirq.Circuit()
    
    for moment in circuit.moments:
        for op in moment.operations:
            # Check if operation has unassigned parameters
            has_unassigned_param = False
            
            # For parameterized gates, we need to check if they have unassigned parameters
            if hasattr(op.gate, '_exponent') and isinstance(op.gate._exponent, cirq.Symbol):
                has_unassigned_param = True
            elif hasattr(op.gate, '_phase_exponent') and isinstance(op.gate._phase_exponent, cirq.Symbol):
                has_unassigned_param = True
            elif hasattr(op.gate, '_angle_rads') and isinstance(op.gate._angle_rads, cirq.Symbol):
                has_unassigned_param = True
            elif hasattr(op.gate, '_theta') and isinstance(op.gate._theta, cirq.Symbol):
                has_unassigned_param = True
            elif hasattr(op.gate, '_phi') and isinstance(op.gate._phi, cirq.Symbol):
                has_unassigned_param = True
            elif hasattr(op.gate, '_lam') and isinstance(op.gate._lam, cirq.Symbol):
                has_unassigned_param = True
            else:
                # Check if any parameter in the gate is a symbol
                for attr_name in dir(op.gate):
                    attr = getattr(op.gate, attr_name)
                    if isinstance(attr, cirq.Symbol):
                        has_unassigned_param = True
                        break
            
            if not has_unassigned_param:
                new_circuit.append(op)
    
    return new_circuit
