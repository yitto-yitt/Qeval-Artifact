# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterExpression

def remove_unassigned_parameterized_gates(circuit):
    # Create a new circuit with the same registers as the input circuit
    new_circuit = QuantumCircuit(*circuit.qregs, *circuit.cregs)
    
    # Iterate through all instructions in the original circuit
    for instruction in circuit.data:
        gate = instruction.operation
        # Check if the gate has any parameters
        if hasattr(gate, 'params') and gate.params:
            # Check if any parameter is unassigned (i.e., is a ParameterExpression)
            has_unassigned_param = False
            for param in gate.params:
                if isinstance(param, ParameterExpression) and len(param.parameters) > 0:
                    has_unassigned_param = True
                    break
            
            # If no unassigned parameters, add the gate to the new circuit
            if not has_unassigned_param:
                new_circuit.append(instruction)
        else:
            # If no parameters, add the gate to the new circuit
            new_circuit.append(instruction)
    
    return new_circuit
