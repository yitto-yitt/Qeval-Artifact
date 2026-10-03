# EVAL_META: task_id=99, framework=cirq, class=3
import cirq
from typing import Union

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = cirq.Circuit()
    
    for moment in circuit.moments:
        for op in moment.operations:
            # Check if operation has unassigned parameters
            has_unassigned_param = False
            
            # For parameterized operations in Cirq, we need to check if any parameter is unbound
            if hasattr(op, 'gate') and hasattr(op.gate, '_num_qubits'):
                # Check if gate is parameterized and has unassigned values
                if hasattr(op.gate, '__getattribute__'):
                    # Look for attributes that indicate parameterization
                    for attr_name in dir(op.gate):
                        attr = getattr(op.gate, attr_name)
                        if hasattr(attr, '__class__') and 'Parameter' in str(type(attr)):
                            has_unassigned_param = True
                            break
            
            # Alternative approach: try to identify common parameterized gates
            gate_str = str(op.gate).lower()
            if 'phaseslip' in gate_str or 'rotation' in gate_str or \
               'xpow' in gate_str or 'ypow' in gate_str or 'zpow' in gate_str or \
               'cphase' in gate_str or 'parity' in gate_str:
                # These are often parameterized - check specifically
                if hasattr(op.gate, 'exponent') and isinstance(op.gate.exponent, (cirq.Symbol, type(cirq.ParamResolver({}).param_dict))):
                    has_unassigned_param = True
                elif hasattr(op.gate, 'angle') and isinstance(op.gate.angle, (cirq.Symbol, type(cirq.ParamResolver({}).param_dict))):
                    has_unassigned_param = True
                elif hasattr(op.gate, 'rads') and isinstance(op.gate.rads, (cirq.Symbol, type(cirq.ParamResolver({}).param_dict))):
                    has_unassigned_param = True
                elif hasattr(op.gate, 'degrees') and isinstance(op.gate.degrees, (cirq.Symbol, type(cirq.ParamResolver({}).param_dict))):
                    has_unassigned_param = True
                elif hasattr(op.gate, 'p') and isinstance(op.gate.p, (cirq.Symbol, type(cirq.ParamResolver({}).param_dict))):
                    has_unassigned_param = True
            else:
                # Check if it's a general parameterized operation
                for param_key in op._circuit_diagram_info_(cirq.CircuitDiagramInfoArgs.UNINFORMED).wire_symbols if hasattr(op, '_circuit_diagram_info_') else []:
                    if isinstance(param_key, cirq.Symbol):
                        has_unassigned_param = True
                        break
            
            # If no unassigned parameters, add to new circuit
            if not has_unassigned_param:
                new_circuit.append(op)
    
    return new_circuit
