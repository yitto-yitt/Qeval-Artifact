# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.parameter import Parameter


def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QuantumCircuit(*circuit.qregs, *circuit.cregs)
    
    for instruction in circuit.data:
        # Check if any parameter in the instruction is an unassigned Parameter
        has_unassigned_param = False
        
        # Get the parameters of the current instruction
        params = instruction.operation.params
        for param in params:
            if isinstance(param, Parameter):
                has_unassigned_param = True
                break
        
        # Only add the instruction if it doesn't have unassigned parameters
        if not has_unassigned_param:
            new_circuit.append(instruction)
    
    return new_circuit
