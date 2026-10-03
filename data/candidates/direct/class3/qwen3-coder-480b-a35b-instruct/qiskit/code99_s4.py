# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.parameter import Parameter


def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QuantumCircuit(*circuit.qregs, *circuit.cregs)
    
    for instruction in circuit.data:
        # Check if the instruction has any unassigned parameters
        has_unassigned_params = False
        
        # Look for parameters in the operation's parameters
        for param in instruction.operation.params:
            if isinstance(param, Parameter):
                has_unassigned_params = True
                break
            elif hasattr(param, 'parameters'):
                # For expressions containing parameters
                if len(param.parameters) > 0:
                    has_unassigned_params = True
                    break
        
        # If no unassigned parameters, add the instruction to the new circuit
        if not has_unassigned_params:
            new_circuit.append(instruction)
    
    return new_circuit
